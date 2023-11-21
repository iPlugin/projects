

































class Cat:
    @classmethod
    def set_name(self, name):
        self.name = name
        print(f"Cat name is {name}")
        
    @staticmethod
    def call():
        print("Murrr")

Cat.set_name("Boris")
Cat.call()

# cat1 = Cat()

# cat1.set_name("Boris")
# cat1.call()