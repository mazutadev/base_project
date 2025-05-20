"""
Module for executing commands through subprocess.
"""

import subprocess
import logging
import shlex
from typing import List, Union

from .value_objects import CommandResult
from .enums import CommandStatus


class CommandExecutor:
    """Class for executing commands through subprocess"""

    def __init__(self, logger: logging.Logger, timeout: int = 300):
        self._logger = logger.getChild("CommandExecutor")
        self.timeout = timeout

    def _prepare_command(
        self,
        command: Union[str, List[str]],
        use_sudo: bool = False,
        use_shell: bool = False,
    ) -> Union[str, List[str]]:
        """
        Prepare command to execute.

        Args:
            command: Command to execute (str or list).
            use_sudo: Whether to prepend 'sudo'.
            use_shell: Whether to use shell.

        Returns:
            Command as string (for shell) or list (for exec).
        """
        if use_shell:
            # В shell-режиме sudo просто добавляется в строку
            if use_sudo:
                if isinstance(command, list):
                    command = " ".join(shlex.quote(arg) for arg in command)
                command = f"sudo {command}"
            elif isinstance(command, list):
                command = " ".join(shlex.quote(arg) for arg in command)
            return command
        else:
            # Без shell: всегда список
            if isinstance(command, str):
                cmd_list = shlex.split(command)
            else:
                cmd_list = list(command)
            if use_sudo:
                return ["sudo"] + cmd_list
            return cmd_list

    def execute(
        self,
        command: Union[str, List[str]],
        use_sudo: bool = False,
        use_shell: bool = False,
        timeout: int = None,
    ) -> CommandResult:
        """
        Execute command.

        Args:
            command: Command to execute (str or list).
            use_sudo: Whether to prepend 'sudo'.
            use_shell: Whether to use shell.

        Returns:
            Command result.
        """

        if timeout is None:
            timeout = self.timeout

        try:
            cmd = self._prepare_command(command, use_sudo, use_shell)
            self._logger.debug(f"Executing command: {cmd} (shell={use_shell})")
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=use_shell,
            )
            stdout, stderr = process.communicate(timeout=timeout)
            return_code = process.returncode

            status = CommandStatus.SUCCESS if return_code == 0 else CommandStatus.FAILED

            return CommandResult(
                status=status,
                stdout=stdout.strip(),
                stderr=stderr.strip(),
                return_code=return_code,
                command=command if isinstance(command, str) else " ".join(command),
            )

        except subprocess.TimeoutExpired:
            process.kill()
            return CommandResult(
                status=CommandStatus.TIMEOUT,
                stdout="",
                stderr=f"Command timed out after {timeout} seconds",
                return_code=-1,
                command=command if isinstance(command, str) else " ".join(command),
            )
        except Exception as e:
            return CommandResult(
                status=CommandStatus.FAILED,
                stdout="",
                stderr=str(e),
                return_code=-1,
                command=command if isinstance(command, str) else " ".join(command),
            )

    def execute_with_prompt(
        self,
        command: Union[str, List[str]],
        prompt: str,
        use_sudo: bool = False,
        use_shell: bool = False,
        timeout: int = None,
    ) -> CommandResult:
        """
        Execute command with prompt.

        Args:
            command: Command to execute (str or list).
            prompt: Prompt to send to stdin.
            use_sudo: Whether to prepend 'sudo'.
            use_shell: Whether to use shell.

        Returns:
            Command result.
        """

        if timeout is None:
            timeout = self.timeout

        try:
            cmd = self._prepare_command(command, use_sudo, use_shell)
            self._logger.debug(
                f"Executing command with prompt: {cmd} (shell={use_shell})"
            )
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                shell=use_shell,
            )
            stdout, stderr = process.communicate(input=prompt + "\n", timeout=timeout)
            return_code = process.returncode

            status = CommandStatus.SUCCESS if return_code == 0 else CommandStatus.FAILED

            return CommandResult(
                status=status,
                stdout=stdout.strip(),
                stderr=stderr.strip(),
                return_code=return_code,
                command=command if isinstance(command, str) else " ".join(command),
            )

        except subprocess.TimeoutExpired:
            process.kill()
            return CommandResult(
                status=CommandStatus.TIMEOUT,
                stdout="",
                stderr=f"Command timed out after {timeout} seconds",
                return_code=-1,
                command=command if isinstance(command, str) else " ".join(command),
            )
        except Exception as e:
            return CommandResult(
                status=CommandStatus.FAILED,
                stdout="",
                stderr=str(e),
                return_code=-1,
                command=command if isinstance(command, str) else " ".join(command),
            )
