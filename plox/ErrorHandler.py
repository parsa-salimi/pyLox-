from TokenType import TokenType

class LoxRuntimeError(RuntimeError):
    def __init__(self, token, message):
        self.token = token
        super().__init__(message)


class ErrorHandler:

    had_error = False
    hadRuntimeError = False

    @staticmethod
    def report(line,where, message):
        print("[line" + str(line) + "] Error" + where + ": " + message)
        ErrorHandler.had_error = True

    @staticmethod
    def set_error_field(state):
        ErrorHandler.had_error = state

    @staticmethod
    def error( line, message):
        ErrorHandler.report(line, "", message)



    @staticmethod
    def TokenError( token, message):
        if (token.type == TokenType.EOF):
            ErrorHandler.report(token.line, " at end", message)
        else : ErrorHandler.report(token.line, " at '" + token.lexeme + "'", message)

    @staticmethod
    def runtimeError( err):
        print(str(err) + "\n[ line " + str(err.token.line) + "]")
        ErrorHandler.hadRuntimeError = True