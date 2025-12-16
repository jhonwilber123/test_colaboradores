class Prompt:

    def __init__(
        self, 
        uid: str, 
        name: str, 
        instructions: str, 
        
    ) -> None:
        self.uid = uid
        self.name = name
        self.instructions = instructions