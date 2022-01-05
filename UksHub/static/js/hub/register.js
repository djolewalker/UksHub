(() => {
  const password = document.getElementById("id_password");
  const repeatPassowrd = document.getElementById("repeat_password");

  const check = () => {
    if (
      document
        .getElementsByClassName("needs-validation")[0]
        .classList.contains("was-validated")
    ) {
      if (password.value == repeatPassowrd.value) {
        repeatPassowrd.classList.remove("is-invalid");
        repeatPassowrd.classList.add("is-valid");
        repeatPassowrd.setCustomValidity("");
      } else {
        repeatPassowrd.classList.add("is-invalid");
        repeatPassowrd.classList.remove("is-valid");
        repeatPassowrd.setCustomValidity("Error");
      }
    }
  };

  password.addEventListener("keyup", check);
  repeatPassowrd.addEventListener("keyup", check);
  Array.prototype.slice
    .call(document.querySelectorAll(".needs-validation"))
    .forEach((form) => {
      form.addEventListener(
        "submit",
        (event) => {
          if (!form.checkValidity() || password.value != repeatPassowrd.value) {
            event.preventDefault();
            event.stopPropagation();
          }
          check();
          form.classList.add("was-validated");
        },
        false
      );
    });
})();
