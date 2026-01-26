import sys
import Network_Security.logging.logger as logger

class NetworkSecurityException(Exception):
    """Base exception class for network security errors."""
    def __init__(self,error_message,error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in script: {self.file_name} at line number: {self.lineno} with message: {self.error_message}".format(
        self.file_name, self.lineno, str(self.error_message))
    