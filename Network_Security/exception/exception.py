import sys
import Network_Security.logging.logger as logger

class NetworkSecurityException(Exception):
    """Base exception class for network security errors."""
    def __init__(self, error_message, error_details: sys = None):
        super().__init__(error_message)
        self.error_message = error_message
        self.lineno = -1
        self.file_name = "<unknown>"

        if error_details is not None:
            _, _, exc_tb = error_details.exc_info()
            if exc_tb is not None:
                self.lineno = exc_tb.tb_lineno
                self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in script: {self.file_name} at line number: {self.lineno} with message: {self.error_message}".format(
        self.file_name, self.lineno, str(self.error_message))
    
