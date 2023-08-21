import discord
from discord import app_commands
import os

import azuregpt
import midjourney
import memerator

import asyncio

# load environment variables 
from dotenv import load_dotenv
load_dotenv()

# 测试服务器guild=discord.Object(id=1141703937225924688)
# 所有服务器通用guild=None
discord_guild = None


class MyClient(discord.Client):

  def __init__(self):
    intents = discord.Intents.default()
    intents.message_content = True
    super().__init__(intents=intents)
    self.synced = False
    self.mjclient = midjourney.MJ()

  async def on_ready(self):
    # when bot is ready
    await self.wait_until_ready()
    if not self.synced:
      await tree.sync(guild=discord_guild)
      self.synced = True
    print(f'We have logged in as {self.user}')

  async def on_message(self, message):
    # when bot receive a message
    if message.author == client.user:
      return

    if message.content.startswith('$hello'):
      await message.channel.send('Hello!')

  async def handle_meme_command(self, prompt, user_id, interaction):
    mention = f"<@{user_id}>"

    values = await azuregpt.getMemeContent(prompt)
    if values is not None:
      print("------------------------------------------")
      top, bottom, image = values
      print("TOP:", top)
      print("BOTTOM:", bottom)
      print("IMAGE:", image)
      print("------------------------------------------")

      generate_task_id = self.mjclient.subimt_image_api(image)
      print("generate:", generate_task_id)
      generate_image = await self.wait_for_task_completion(generate_task_id)
      print("generated:", generate_task_id)
      upscale_task_id = self.mjclient.upscale_image_api(1, generate_task_id)
      print("upscale:", upscale_task_id)
      upscale_image = await self.wait_for_task_completion(upscale_task_id)
      print("upscaled:", upscale_task_id)

      async def splice_image():
        file_path = memerator.splice_text_image(user_id, upscale_image, top,
                                                bottom)
        file = discord.File(file_path)

        print("------------------------------------------")
        print("用户", user_id, "任务完成")
        print("------------------------------------------")

        await interaction.followup.send(
          content=f"**{prompt}** - {mention} \n ", file=file)

      if generate_image is None or upscale_image is None:
        print("------------------------------------------")
        print("用户", user_id, "任务失败，请重试")
        print("------------------------------------------")
        await interaction.response.edit_message(
          f"Whoops, that didn't quite work out! Let's give it another whirl, shall we? - {mention}"
        )

      else:
        asyncio.create_task(splice_image())

    else:
      print("------------------------------------------")
      print("用户", user_id, "任务失败，请重试")
      print("------------------------------------------")
      await interaction.response.edit_message(
        f"Whoops, that didn't quite work out! Let's give it another whirl, shall we? - {mention}"
      )

  async def wait_for_task_completion(self, task_id):
    while True:
      data = self.mjclient.check_progress_by_id(task_id)
      progress = data["progress"]
      status = data["status"]
      if progress == "100%":
        print(task_id, "---", progress)
        return data["imageUrl"]
      else:
        if status == "FAILURE":
          return None
        print(task_id, "---", progress)
        await asyncio.sleep(5)


client = MyClient()
tree = app_commands.CommandTree(client)


@tree.command(name="meme",
              description="get a meme by prompt",
              guild=discord_guild)
async def self(interaction: discord.Integration, prompt: str):
  print("------------------------------------------")
  print("收到来自用户", interaction.user.id, "的meme图命令")
  print("------------------------------------------")
  await interaction.response.send_message(
    "Hang tight! Your task is doing the cha-cha slide into our system. We'll be back faster than a popcorn pop!"
  )
  await client.handle_meme_command(prompt, interaction.user.id, interaction)


client.run(os.getenv('DISCORD_BOT_TOKEN'))
