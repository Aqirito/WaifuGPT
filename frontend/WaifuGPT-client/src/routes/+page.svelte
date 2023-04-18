<script lang="ts">
  import { onMount } from "svelte";
  import { ApiService } from "../lib/services/apiService";
  import { browser } from "$app/environment";
  export const apiService = new ApiService();

  let webkitrecognition: any;
  let texts: any;
  let chat: any;
  let chat_bubble: any
  let chat1: any;
  let chat_bubble1: any
  let buttonLoad: any
  let buttonStartSpeech: any
  let embed: any
  let isStart = false;
  let isLanguage: boolean = true;
  let chat_history: any = {
    "history": []
  };

  onMount(() => {
    embed = document.createElement("embed") as HTMLEmbedElement;
    embed.setAttribute("loop", "true");
    embed.setAttribute("autostart", "true");
    embed.setAttribute("height", "2");
    embed.setAttribute("width", "0");
    embed.style.position = "absolute";

    texts = window.document.getElementById("texts") as HTMLDivElement;
    loadSpeechRecog()
  })
  function loadSpeechRecog() {

    if (!('webkitSpeechRecognition' in window)) {
      console.log('Speech recognition not available');
      return;
    }
    webkitrecognition = new (window as any).webkitSpeechRecognition();
    webkitrecognition.interimResults = true;
    webkitrecognition.addEventListener("result", (e: any) => {
      let text = Array.from(e.results)
        .map((result: any) => result[0])
        .map((result: any) => result.transcript)
        .join("");

      if (e.results[0].isFinal) {
        console.log("input speech: ", text);

        if (text.toLowerCase().includes("izumi")) {
          createChatElement(text)
        }
      }
    });
    buttonLoad.classList.add("btn-success")
    
    webkitrecognition.addEventListener("end", () => {
      if (isStart) {
        webkitrecognition.start();
      }
    })
    webkitrecognition.addEventListener("start", () => {
      if (isLanguage) {
        console.log("is language", isLanguage)
        webkitrecognition.lang = "en-us"
      } else {
        console.log("is language", isLanguage)
        webkitrecognition.lang = "ms-my"
      }
    })
  }

  function createChatElement(text: any) {
    chat = document.createElement("div") as HTMLDivElement;
    chat.classList.add("chat")
    chat.classList.add("chat-end")
    chat_bubble = document.createElement("div") as HTMLDivElement;
    chat_bubble.classList.add("chat-bubble");
    chat_bubble.classList.add("chat-bubble-primary");
    texts.appendChild(chat);
    chat_bubble.innerText = text;
    chat.appendChild(chat_bubble)
    synthesize(text);
    chat_history.history.push(`You: ${text}`)
    texts.scrollTop = texts.scrollHeight;
  }

  let input_message: any = ""
  async function synthesize(message: any) {

    let response = await apiService.postMesage(message)
    let bot_reply = response.bot_reply
    let bot_reply_only = bot_reply.split(": ")[1]
    chat_history.history.push(bot_reply)

    chat1 = document.createElement("div") as HTMLDivElement;
    chat1.classList.add("chat")
    chat1.classList.add("chat-start")
    chat1.innerHTML = `
                      <div class="chat-image avatar">
                        <div class="w-10 rounded-full">
                          <img src="Sagiri.png" />
                        </div>
                      </div>
                      <div class="chat-bubble chat-bubble-secondary">${bot_reply_only}</div>
                      <div class="chat-footer opacity-50">
                          ${response.emotions || ""}
                      </div>
                      `
    loadAudio(response.audio)
    texts.appendChild(chat1);
    texts.scrollTop = texts.scrollHeight;
  }

  function loadAudio(response_audio: any) {
    let audioBytes = atob(response_audio);
    let audioArray = new Uint8Array(audioBytes.length);
    for (let i = 0; i < audioBytes.length; i++) {
      audioArray[i] = audioBytes.charCodeAt(i);
    }
    let audioBlob = new Blob([audioArray], { type: 'audio/wav' });
    let audioUrl = URL.createObjectURL(audioBlob);
    embed.setAttribute("src", audioUrl);
    document.body.appendChild(embed);
    // TODO pause recording when the audio is currently playing
  }

  function startStopRecognition() {
    if (webkitrecognition) {
      isStart = !isStart;
      if (!isStart) {
        webkitrecognition.stop();
        console.log("stopped")
        buttonStartSpeech.classList.remove("btn-error")
      } else if (isStart) {
        console.log("start")
        webkitrecognition.start();
        buttonStartSpeech.classList.add("btn-error")
      }
    }
  }

  function newLineText(e: any) {
    // console.log(e)
    const chatInput = document.getElementById(
      "chat-input"
    ) as HTMLTextAreaElement;
    if (e.key === "Enter" && e.shiftKey || e.key === "Enter") {
      e.preventDefault();
      chatInput.value += "\n";
      chatInput.rows += 1;
    }
    if (e.key === "Backspace") {
      if (chatInput.rows === 1) {
        chatInput.rows = 1
        return
      }
      chatInput.rows -= 1;
    }
    if (e.key === "Enter" && e.ctrlKey) {
      createChatElement(input_message)
      chatInput.value = ""
      chatInput.rows = 1
    }
  }

  async function saveChatHistory() {
    const jsonData: string = JSON.stringify(chat_history);
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = 'chat_history.json';
    link.href = url;
    document.body.appendChild(link);
    link.click();
  }
</script>
<section>
  <h1>WaifuGPT</h1>
  <p>beta version</p>
</section>
<div class="md:container md:mx-auto h-screen w-screen">
  <div class="flex">
    <label class="cursor-pointer label">
      <span class="label-text mr-2">MY</span> 
      <input bind:checked={isLanguage} type="checkbox" class="toggle" />
      <span class="label-text ml-2">EN</span> 
    </label>
  </div>
  <div class="mockup-window border bg-base-300 h-custom my-4">
    <div id="texts" class="py-16 px-4 h-full overflow-y-auto">
      <!-- <div class="chat chat-end">
        <div class="chat-image avatar">
          <div class="w-10 rounded-full">
            <img src="https://via.placeholder.com/250" />
          </div>
        </div>
        <div class="chat-bubble chat-bubble-primary">
          It was said that you would, destroy the Sith, not join them.
        </div>
      </div>
      <div class="chat chat-start">
        <div class="chat-image avatar">
          <div class="w-10 rounded-full">
            <img src="https://via.placeholder.com/250" />
          </div>
        </div>
        <div class="chat-bubble">
          It was you who would bring balance to the Force
        </div>
      </div> -->
    </div>
  </div>
  <div class="btn-group">
    <button class="btn btn-active">WAIFU</button>
    <button class="btn">Expert</button>
    <button class="btn" on:click={() => saveChatHistory()}>Save Chat History</button>
  </div>
  <div class="btn-group float-right">
    <button bind:this={buttonLoad} class="btn" on:click={() => loadSpeechRecog()}>Load Speech recognition</button>
    <label bind:this={buttonStartSpeech} class="btn swap">
      <input on:click={() => startStopRecognition()} type="checkbox" />
      <svg class="w-6 h-6 swap-off" fill="none" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
      </svg>      
      <svg class="w-6 h-6 swap-on heartbeat-icon" fill="none" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" stroke-width="1.5" stroke="yellow">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
      </svg>  
    </label>
  </div>
  <div class="mockup-code h-auto my-4 w-full p-4">
    <pre><code>hold 'CTRL' and 'ENTER' to submit</code></pre>
    <textarea
      id="chat-input"
      on:keydown={(e) => newLineText(e)}
      placeholder="Type here and hold CTRL and ENTER to submit"
      class="textarea textarea-secondary w-full resize-y"
      bind:value={input_message}
      rows=1
    />
  </div>
</div>
