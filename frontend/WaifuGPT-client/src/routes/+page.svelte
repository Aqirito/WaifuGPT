<script lang="ts">
  import { ApiService } from "../lib/services/apiService";
  export const apiService = new ApiService();

  let webkitrecognition: any;
  let texts: any;
  let chat: any;
  let chat_bubble: any
  let chat1: any;
  let chat_bubble1: any
  let buttonLoad: any
  let buttonStartSpeech: any
  function loadSpeechRecog() {

    if (!('webkitSpeechRecognition' in window)) {
      console.log('Speech recognition not available');
      return;
    }
    webkitrecognition = new (window as any).webkitSpeechRecognition();
    webkitrecognition.interimResults = true;
    webkitrecognition.addEventListener("result", (e: any) => {
      const text = Array.from(e.results)
        .map((result: any) => result[0])
        .map((result: any) => result.transcript)
        .join("");

      if (e.results[0].isFinal) {
        createChatElement(text)
        // console.log("sd", text);
        // if (text.toLowerCase().includes("hey, milo") || text.toLowerCase().includes("hello milo")) {
        // }
        // p = document.createElement("p");
      }
    });
      
    webkitrecognition.addEventListener("end", () => {
      webkitrecognition.start();
    });
    buttonLoad.classList.add("btn-active")
  }

  function createChatElement(text: any) {
    texts = window.document.getElementById("texts") as HTMLDivElement;
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
  }

  let input_message: any = ""
  async function synthesize(message: any) {
    let response = await apiService.postMesage(message)
    chat1 = document.createElement("div") as HTMLDivElement;
    chat_bubble1 = document.createElement("div") as HTMLDivElement;
    chat1.classList.add("chat")
    chat1.classList.add("chat-start")
    chat_bubble1.classList.add("chat-bubble")
    chat_bubble1.classList.add("chat-bubble-secondary")
    chat1.appendChild(chat_bubble1)
    // p = document.createElement("p");
    // p.classList.add("replay");
    chat_bubble1.innerText = response.bot_res;
    texts.appendChild(chat1);
  }

  function startRecognition() {
    webkitrecognition.start();
    buttonStartSpeech.classList.add("btn-success")
    // buttonStartSpeech.classList.add("btn-active")
  }

  function newLineText(e: any) {
    let lastScrollHeight = 0;
    const chatInput = document.getElementById(
      "chat-input"
    ) as HTMLTextAreaElement;
    if (e.key === "Enter" && e.shiftKey) {
      e.preventDefault();
      chatInput.value += "\n";
      chatInput.style.height = `${chatInput.scrollHeight}px`;
      lastScrollHeight = chatInput.scrollHeight;
    } else if (e.key === "Backspace") {
      chatInput.style.height =
        Math.max(chatInput.scrollHeight / 1.2, lastScrollHeight) + "px";
    } else if (e.key === "Enter") {
      createChatElement(input_message)
      chatInput.value = ""
      chatInput.style.height = "0px"
    }
  }
</script>

<section>
  <h1>WaifuGPT</h1>
  <p>beta version</p>
</section>
<div class="md:container md:mx-auto h-screen w-screen">
  <div class="mockup-window border bg-base-300 h-custom my-4">
    <div id="texts" class="p-16 flex flex-col-reverse h-full overflow-y-auto">
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
    <button class="btn btn-active">Casual</button>
    <button class="btn">Expert</button>
    <button class="btn">Code Assistant</button>
  </div>
  <div class="btn-group float-right">
    <button bind:this={buttonLoad} class="btn" on:click={() => loadSpeechRecog()}>Load Speech recognition</button>
    <button bind:this={buttonStartSpeech} class="btn" on:click={() => startRecognition()}>Start conversation</button>
  </div>
  <div class="mockup-code h-auto my-4 w-full p-4">
    <textarea
      id="chat-input"
      on:keydown={(e) => newLineText(e)}
      placeholder="Type here and press enter to submit"
      class="textarea textarea-secondary w-full resize-y"
      bind:value={input_message}
    />
  </div>
</div>
