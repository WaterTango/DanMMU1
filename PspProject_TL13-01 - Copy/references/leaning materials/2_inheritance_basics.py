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
        print(self.name + " is " + str(dog_years) + " years old in dog years " )




class Beagle(Dog):
    #class to represent a specific (child ) Dog
    def __init__(self,my_name , my_gender, my_age, is_gun_shy):
        #call super parent initialization cl ass (DOG)
        super().__init__(my_name , my_gender, my_age)   
        self.is_gun_shy = is_gun_shy   
    
    def hunt(self):
        if not self.is_gun_shy:
            self.bark(True)
            print(self.name + " just brought back a duck ")
        else:
            print(self.name + " is not a good hunting dog")
    
    def barl(self, is_loud):
        if is_loud:
            print("HOWL HOWL HOWWWWWWWWWWWWWWLLLLLLLLLLLLLLLLL")
        else:
            print("howl")



beagle = Beagle ("kady" , "female" , 10 ,False)
beagle.eat()
beagle.bark(False)
beagle.compute_age()
beagle.hunt()
