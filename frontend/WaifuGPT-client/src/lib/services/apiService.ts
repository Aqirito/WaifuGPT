export class ApiService {
  BaseApiUrl = import.meta.env.VITE_API_BASE_URL;
  VoiceVoxApiUrl = import.meta.env.VITE_VXAPI_BASE_URL;
  headerOptions = {
    'Content-Type': 'application/json; charset=utf-8',
  };

  constructor() {}

  async postMesage(message:string) {
    const payload = {
      messageText: message
    }
    const result = await fetch(`${this.BaseApiUrl}/api/waifu/chats`, {
      method: 'POST',
      headers: new Headers(this.headerOptions),
      body: JSON.stringify(payload)
    });
    if (!result.ok) {
      return new Response(JSON.stringify(result));
    }
    return result.json()
  }
}