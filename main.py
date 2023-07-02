import json
import aiohttp

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

@app.get("/jokes/<string:username>")
async def get_joke(username):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit') as resp:
            joke_data = await resp.json()
            if joke_data["type"] == "twopart":
                joke = f'{joke_data["setup"]} {joke_data["delivery"]}'
            else:
                joke = joke_data["joke"]
            
            print( f'joke is:{joke}')
            return quart.Response(response=json.dumps({"joke": joke}), status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
