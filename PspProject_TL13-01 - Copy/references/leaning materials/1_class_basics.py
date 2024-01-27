class Dog():
    def __init__( self, my_name , my_gender , my_age):
        self.name = my_name
        self.gender = my_gender
        self.age = my_age


    def eat(self):
        if self.gender == "male":
            print("Here " + self.name + "! Good Boy! Eat up")
        else:
            print("Here " + self.name + "! Good Girl! Eat up")

    def bark(self , is_loud):
        if is_loud:
            print("WOOF WOOF WOOF WOOF WOOF")
        else:
            print("woof...")
        
    def compute_age(self):
        dog_years = self.age*7
        print(self.name + "is" + str(dog_years) + "years old in god years " )
