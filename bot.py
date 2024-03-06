from openai import OpenAI
import os
import json
import time
import discord
import random


intents = discord.Intents.all()
DiscordClient = discord.Client(command_prefix="!", intents=intents)

assistant_id = "YOURASSISTANTIDHERE"  # or a hard-coded ID like "asst-..."

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

def show_json(obj):
    print(json.dumps(obj, indent=4))

# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()

def get_most_recent_gpt_response(data):
    # Iterate over messages in reverse to find the most recent GPT response
    for m in data:
        if m.role =="assistant":
            return (f"{m.content[0].text.value}")

# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

# show_json(client)
# print(f'EnvironmentVar: {os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>")}')

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(assistant_id, thread, user_input)
    return thread, run

@DiscordClient.event
async def on_ready():
    print("We have logged in as {0.user}".format(DiscordClient))

@DiscordClient.event
async def on_message(message):
        # if message.content.startswith("hi"):
    #     await message.channel.send("Hello!")
    if message.author == DiscordClient.user:
        return
    
    if "eris" in message.content.lower():
        # Generate a random number between 1 and 10 (inclusive)
        # if random.randint(1, 10) == 1:
        # userInput = input("")
        thread, run = create_thread_and_run(message.content)
        run = wait_on_run(run, thread)

        jsonresponse =(get_response(thread))
        await message.channel.send(get_most_recent_gpt_response(jsonresponse))
    elif random.randint(1, 10) == 1 and "?" in message.content.lower():
        thread, run = create_thread_and_run(message.content)
        run = wait_on_run(run, thread)

        jsonresponse =(get_response(thread))
        await message.channel.send(get_most_recent_gpt_response(jsonresponse))

    elif random.randint(1, 10) == 1:
        thread, run = create_thread_and_run(message.content)
        run = wait_on_run(run, thread)

        jsonresponse =(get_response(thread))
        await message.channel.send(get_most_recent_gpt_response(jsonresponse))

@DiscordClient.event
async def on_guild_join(guild):
        if guild.system_channel:
            await guild.system_channel.send('Hello my name is Eris- ')

DiscordClient.run("YOURDISCORDTOKENHERE")
