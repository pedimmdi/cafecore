document.addEventListener("DOMContentLoaded", () => {

    const messages = document.querySelectorAll(".message");

    messages.forEach(message => {

        const closeButton = message.querySelector(".message-close");

        if(closeButton){

            closeButton.addEventListener("click", () => {

                message.remove();

            });

        }

        setTimeout(() => {

            if(message){

                message.remove();

            }

        },5000);

    });

});