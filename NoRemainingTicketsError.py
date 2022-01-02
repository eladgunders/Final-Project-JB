class NoRemainingTicketsError(Exception):
    def __init__(self, message="No remaining tickets for this flight."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
