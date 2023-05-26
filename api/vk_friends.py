from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

from vk_token import VK_API_KEY


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>VK User Friends</title>
        <script>
            async function getFriends() {
                const inputField = document.getElementById("vkID");
                const vkID = inputField.value;
                const response = await fetch("/friends/" + vkID);
                const friends = await response.json();

                let friendsList = document.getElementById("friendsList");
                friendsList.innerHTML = "";  // clear existing list
                
                for (let friend of friends) {
                    let friendItem = document.createElement("li");
                    friendItem.innerHTML = `<a href="https://vk.com/id${friend.id}">
                                                <img src="${friend.photo_50}" alt="Avatar">
                                                ${friend.first_name} ${friend.last_name}
                                            </a>`;
                    friendsList.appendChild(friendItem);
                }
            }
        </script>
    </head>
    <body>
        <input id="vkID" type="text" placeholder="Enter VK id or username">
        <button onclick="getFriends()">Get Friends</button>
        <ul id="friendsList"></ul>
    </body>
    </html>
    """


@app.get("/friends/{vk_id}")
async def get_friends(vk_id: str):
    if not vk_id.isdigit():
        url = f"https://api.vk.com/method/users.get?user_ids={vk_id}&access_token={VK_API_KEY}&v=5.130"
        response = requests.get(url)
        vk_id = response.json()["response"][0]["id"]
    url = f"https://api.vk.com/method/friends.get?user_id={vk_id}&fields=first_name,last_name,photo_50&access_token={VK_API_KEY}&v=5.130"
    response = requests.get(url)
    return response.json()["response"]["items"]
