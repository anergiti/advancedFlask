def post(self, name):
      if next(filter(lambda x: x['name'] == name,items), None) is not None:
          return {'message': "An item with name '{}' already exists". format(name)}, 400

      data = request.get_json()
      # get data form the request ^
      item = {'name': name, 'price': data['price']}
      items.append(item)
      return item , 201

      APP_ROOT = os.path.dirname(os.path.abspath(__file__))
      @app.route("/uploadfile", methods=['POST','PUT'])
      def hello():
          target = os.path.join(APP_ROOT,'files/')
          file = request.files['filedata']

          #if file and allowed_file(file.filename):
          filename=secure_filename(file.filename)
          print(filename)
          destination = "/".join([target, filename])
          print(destination)
          file.save(destination)
          return "Success"
