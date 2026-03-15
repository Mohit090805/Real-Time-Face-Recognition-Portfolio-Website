document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("video");
    const btn = document.getElementById("scan-btn");

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => video.srcObject = stream)
        .catch(err => alert("Cannot access webcam: " + err));

    btn.addEventListener("click", async () => {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;

        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = canvas.toDataURL("image/jpeg");

        try {
            const res = await fetch('/api/verify-face', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: imageData })
            });

            const data = await res.json();
            console.log("Face verification response:", data);

            if (data.success) window.location.href = "/";
            else alert("Access Denied");
        } catch (err) {
            console.error(err);
            alert("Error contacting server");
        }
    });
});
