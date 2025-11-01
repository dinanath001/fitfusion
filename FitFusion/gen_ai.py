import mimetypes
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"✅ File saved to: {file_name}")


def generate_slogan(client):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Write a short catchy motivational slogan about fitness and positivity."
    )
    slogan = response.candidates[0].content.parts[0].text.strip()
    print("\n💡 AI Generated Slogan:", slogan)
    return slogan


def generate_poster(client, slogan):
    instruction = f"Create a colorful fitness motivational poster with this slogan in bold text: '{slogan}'"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=instruction)],  # ✅ yaha fix
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],  # ✅ Sirf IMAGE
    )

    file_index = 0
    for chunk in client.models.generate_content_stream(
        model="gemini-1.5-flash",
        contents=contents,
        config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content.parts:
            continue

        part = chunk.candidates[0].content.parts[0]

        if part.inline_data and part.inline_data.data:
            file_name = f"fitness_poster_{file_index}"
            file_index += 1
            inline_data = part.inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            save_binary_file(f"{file_name}{file_extension}", data_buffer)




if __name__ == "__main__":
    # 👇 Yaha apni Google Cloud Console se valid API key dalo
    client = genai.Client(api_key="AIzaSyCsmztPkKv5ItFdWatCNXIoa4K_l9TIHbU")

    slogan = generate_slogan(client)
    generate_poster(client, slogan)
