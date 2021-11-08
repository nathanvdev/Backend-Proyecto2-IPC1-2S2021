from flask import Flask, json, jsonify, request
from flask_cors import CORS
from User import User, Post
import re


Users = []
file = []


app = Flask(__name__)
app.config['UPLOAD_FOLDER']="./"
CORS(app)

Users.append(User("Abner Cardona", "M", "admin", "admin@ipc1.coma", " admin@ipc1"))
Users.append(User("Nathan Valdez", "M", "VosNathan", "nathanvaldez413@gmail.com", "admin"))


@app.route('/NewUser', methods=['POST'])
def NewUser():

    global Users
    global User
    

    Name = request.json['name']
    Gender = request.json['gender']
    Username = request.json['username']
    Email = request.json['email']
    Password = request.json['password']

    Characters = "^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[@$!%#?&])[A-Za-z\d@$!#%?&]{8,20}$"
    pat = re.compile(Characters)
    Agree = re.search(pat,Password)
    if Agree:
        print('Validacion Aprovada')   
    else:
        return jsonify({'mensaje':'La Contraseña debe contener 8 caracteres, un simbolo y un numero',})
    
    if Name == '' or Username == '' or Email == '' or Password == '':
        return jsonify({'mensaje': 'Por favor llenar todos los campos'})

    for User1 in Users:
        if User1.getUsername() == Username:
            return jsonify({'mensaje': 'Nombre de usuario ya existente'})
        if User1.getEmail() == Email:
            return jsonify({'mensaje': 'Correo Electronico ya existente'})

   

    #newUser = User(Name, Gender, Username, Email, Password)
    Users.append(User(Name, Gender, Username, Email, Password))

    return jsonify({'mensaje': 'Usuario agregado correctamente por favor inicie sesion'})

@app.route('/GetUsers', methods=['GET'])
def GetUsers():
    global Users

    Datos = []

    for User in Users:
        objeto ={
            'name': User.getName(),            
            'gender': User.getGender(),
            'username': User.getUsername(),
            'email': User.getEmail(),
            'password': User.getPassword()
        }

        Datos.append(objeto)
    return(jsonify(Datos))

@app.route('/Login', methods=['POST'])
def Login():
    global Users
    global User

    Username = request.json['username']
    Password = request.json['password']

    for User in Users:

        if Username == User.getUsername():
            if Password == User.getPassword():
                return jsonify({'mensaje': 'Si Inició Sesión',
                                'approved': True,
                                'name': User.getName(),
                                'gender': User.getGender(),
                                'username': User.getUsername(),
                                'email': User.getEmail(),
                                'password': User.getPassword(),
                                'posts': User.getPosts()})
            else:
                
                return jsonify({'mensaje': 'Contraseña Incorrecta',
                                'approved': False})
    else:
        
        return jsonify({'mensaje': 'No se encontro el usuario',
                        'approved': False})


@app.route('/ModifyPorfile/<string:username>', methods = ['PUT'])
def ModifyPorfile(username):
    global Users
    global User

    for User in Users:
        if username == User.getUsername():
            User.setName(request.json['name'])
            User.setGender(request.json['gender'])

            Username = request.json['username']
            for Userr in Users:
                if Username != Userr.getUsername() or Username == User.getUsername():
                    User.setUsername(Username)
                else:
                    return jsonify({"mensaje": "El Usuario Ya existe"})
            User.setEmail(request.json['email'])
            User.setPassword(request.json['password'])
            return jsonify({"mensaje": "Se cambiaron los datos correctamente"})
        continue
    else:
        return jsonify({"mensaje": "no se encontro el dato para actualizar"})

@app.route('/NewPost', methods=['POST'])
def NewPost():
    global Users
    global User

    Url = request.json['url']
    Date = request.json['date']
    Category = request.json['category']
    Author = request.json['author']
    Type = request.json['type']

    newPost = Post(Url, Date, Category, Type)
    
    print('*****', Author)

    for User in Users:
        print(User.getUsername())
        if Author == User.getUsername():
            User.addPost(newPost)
            return jsonify({"mensaje": "Se agrego el nuevo post"})
        continue
    else:
        return jsonify({"mensaje": "no se encontro el dato para actualizar"})
    
@app.route('/UploadUsers', methods=['POST'])
def UploadUsers():

    global Users
    global User

    global file
    
    file = request.json['UploadUsersp']
    load = json.loads(file)

    for NewUser in load:

        Name = NewUser['name']
        Gender = NewUser['gender']
        Username = NewUser['username']
        Email = NewUser['email']
        Password = NewUser['password']
        
        Users.append(User(Name, Gender, Username, Email, Password))

    return jsonify({"mensaje": "Usuarios cargados"})


@app.route('/UploadPost', methods=['POST'])
def UploadPost():
    global Users
    global User

    global file
    
    file = request.json['UploadPostsp']
    load = json.loads(file)

    for NewPost in load['images']:

        Url = NewPost['url']
        Date = NewPost['date']
        Category = NewPost['category']
        Author = NewPost['author']
        
        for User in Users:
            
            if Author == User.getUsername():
                User.addPost(Post(Url,Date,Category, 'image'))
                
    
    for NewPost in load['videos']:
    
        Url = NewPost['url']
        Date = NewPost['date']
        Category = NewPost['category']
        Author = NewPost['author']
        
        for User in Users:
            
            if Author == User.getUsername():
                User.addPost(Post(Url,Date,Category, 'video'))
                
                

    
    return jsonify({"mensaje": "Posts Cargados"})


@app.route('/Home', methods=['GET'])
def GetPosts():
    global Users
    global User

    Datos = []

    for User in Users:

        for Post in User.getPosts():
            
            objeto ={
            'url': Post.getUrl(),            
            'date': Post.getDate(), 
            'category': Post.getCategory(), 
            'author': User.getUsername(), 
            'type': Post.getType(),
            'numLikes': Post.getLikes(),
            'nameAuthor': User.getName(),
            'serienumber': Post.getSerieNumber()
            }

            Datos.append(objeto)


    return(jsonify(Datos))


@app.route('/Like/<string:UrlIn>', methods=['PUT'])
def AddLike(UrlIn):

    global Users
    global User

    for User in Users:
        for Post in User.getPosts():
            if UrlIn == Post.getSerieNumber():

                Post.setLike(1) 
                print(Post.getLikes())

                return jsonify({'Mensaje':'Se Agrego un like a '})

    return jsonify({'Mensaje':'No se encontro el dato para actualizar'})


@app.route('/PostsUser/<string:UserPosts>', methods=['GET'])
def PostsUser(UserPosts):
    global Users
    global User

    Datos = []

    for User in Users:

        if UserPosts == User.getUsername():
            
            for Post in User.getPosts():
                
                objeto ={
                'url': Post.getUrl(),            
                'date': Post.getDate(), 
                'category': Post.getCategory(), 
                'author': User.getUsername(), 
                'type': Post.getType(),
                'numLikes': Post.getLikes(),
                'nameAuthor': User.getName(),
                'serienumber': Post.getSerieNumber()
                }

                Datos.append(objeto)


    return(jsonify(Datos))


@app.route('/DeleteUser/<string:user>', methods=['DELETE'])
def EliminarPersona(user):

    global Users
    global User

    for User in Users:

        if user == User.getUsername():

            Users.remove(User)

            return jsonify({'mensaje':'Se elimino el dato exitosamente'})
          
    return jsonify({'mensaje':'No se encontro el dato para eliminar'})

@app.route('/AdminMod/<string:user>', methods=['GET'])
def AdmModify(user):
    print(user)
    global Users
    global User

    for User in Users:
        print(User.getUsername())

        if user == User.getUsername():

            objeto ={
                'name': User.getName(),            
                'gender': User.getGender(),
                'username': User.getUsername(),
                'email': User.getEmail(),
                'password': User.getPassword()
            }
            return(jsonify(objeto))
    else:
         return jsonify({'mensaje':'No se encontro el Usuario'})

@app.route('/DeletePost/<string:user>/<string:serie>', methods=['DELETE'])
def EliminarPost(user, serie):

    global Users
    global User

    for User in Users:

        if user == User.getUsername():

            for Post in User.getPosts():

                if serie == Post.getSerieNumber():

                    User.getPosts().remove(Post)

                    return jsonify({'mensaje':'Se elimino el dato exitosamente'})
          
    return jsonify({'mensaje':'No se encontro el dato para eliminar'})

@app.route('/AdminNewPost/<string:user>/<string:serie>', methods=['GET'])
def AdmModifyPost(user, serie):
    print(user)
    global Users
    global User

    for User in Users:

        if user == User.getUsername():

            for Post in User.getPosts():

                if serie == Post.getSerieNumber():

                    objeto ={
                        'url': Post.getUrl(),            
                        'date': Post.getDate(),
                        'category': Post.getCategory(),
                        'type': Post.getType()
                    }
                    return(jsonify(objeto))
    else:
         return jsonify({'mensaje':'No se encontro el Post'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)