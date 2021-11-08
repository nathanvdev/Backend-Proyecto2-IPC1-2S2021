import uuid
class User:
    
    

    def __init__(self, Name, Gender, Username, Email, Password):
        self.name = Name
        if Gender.lower() == 'm':
            self.gender = True
        else:
            self.gender = False
        self.username = Username
        self.email = Email.lower()
        self.password = Password
        self.Posts = []
        

    def addPost(self, objeto):
        self.Posts.append(objeto)




    #Getters
    def getName(self):
        return self.name

    def getGender(self):
        if self.gender:
            return 'Masculino'
        else:
            return 'Femenino'

    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password
    
    def getPosts(self):
        return self.Posts
    

    #Setters
    def setName(self, Name):
        self.name = Name
        
    def setGender(self, Gender):
        if Gender.lower() == 'm':
            self.gender = True
        else:
            self.gender = False

    def setUsername(self, Username):
        self.username = Username

    def setEmail(self, Email):
        self.email = Email.lower()

    def setPassword(self, Password):
        self.password = Password

    def myself(self):
        print('Nombre: ',self.name)
        if self.gender:
            print('Genero: Masculino')
        else:
            print('Genero: Femenino')

        print('user: ',self.username)
        print('email: ',self.email)
        print('password: ',self.password)
        print('--------------------------------')
        print('')

        

    def ModifyPorfile(self, Name, LastName, Password):
        self.name = Name
        self.name += '', LastName
        self.password = Password
        
        
class Post:
    def __init__(self, URL, Date, Category, Type):
        self.url = URL
        self.date = Date
        self.category = Category
        self.type = Type
        self.NumLikes = 0
        self.serie = uuid.uuid4()

    #Getters
    def getUrl(self):
        return self.url

    def getDate(self):
        return self.date

    def getCategory(self):
        return self.category
    
    def getType(self):
        return self.type

    def getLikes(self):
        return str(self.NumLikes) 
    
    def getSerieNumber(self):
        return str(self.serie)
    
    #Setters
    def setUrl(self, URL):
        self.url = URL

    def setDate(self, Date):
        self.date = Date
    
    def setCategory(self, Category):
        self.category = Category
    
    def setType(self, Type):
        self.type = Type      

    def setLike(self, num):
        self.NumLikes += num  
