import engine
from flask import Flask,request,jsonify

app = Flask(__name__)
        

@app.route('/movie', methods=['POST'])
def recommend_movies():
        res = engine.recommend(request.args.get('title'))
        return jsonify(res)

if __name__=='__main__':
        app.run(port=5000)




        


