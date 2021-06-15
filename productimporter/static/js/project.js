var fileUploadInput = document.getElementById("file-upload");

var inputValues = {};
var presignedUrl = '';
var fileName = '';
var fileItemId = ''

window.addEventListener('DOMContentLoaded', (event) => {
  fileUploadInput.addEventListener("change", showFileName);
});

function showFileName(e) {
  const file = fileUploadInput.files[0];
  fileName = file?.name;
  const fileData = { filename: fileName };
  const updatedData = JSON.stringify(fileData);

  fetch("/api/files/policy/", {
    method: "POST",
    body: updatedData,
    headers: {
      "Content-Type": "application/json; charset=UTF-8; ",
    }
  })
    .then((response) => {
      response.json().then((res) => {
        const { url, fields , file_item_id} = res;
        inputValues = fields;
        presignedUrl = url;
        fileItemId = file_item_id;
        document.getElementsByName('upload-s3-button')[0].style['display']='inline';
        // fetch(presignedUrl, {
        //   method: "POST",
        //   body: file,
        // }).then((res) => res.json().then((data) => {
        //     console.log(data, "dataValues");
        //   }))
        //   .catch((error) => console.log(error, "errorValues"))
      })
    })
    .catch((error) => console.log(error, "error fetching presigned url"));

}

var formElement = document.getElementById("upload-to-s3");
formElement.addEventListener("submit", updateFormData);

function updateFormData(event) {
  const input = formElement.elements;
  // const file = fileUploadInput.files[0];
  formElement.action=presignedUrl;
  input.key.value=inputValues.key;
  input.acl.value=inputValues.acl;
  input.Policy.value=inputValues.policy;
  input['X-Amz-Algorithm'].value = inputValues['x-amz-algorithm'];
  input['X-Amz-Credential'].value=inputValues['x-amz-credential'];
  input['X-Amz-Date'].value=inputValues['x-amz-date'];
  input['X-Amz-Signature'].value=inputValues['x-amz-signature'];
}

$('#upload-to-s3').on('submit',function(){
  setTimeout(function() {
    // let data = new URLSearchParams();
    // data.append('key', inputValues.key);
    const fileData = { key: inputValues.key };
    const updatedData = JSON.stringify(fileData);
    fetch("/api/download_csv/", {
      method: "POST",
      body: updatedData,
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
      }
    }).then((res) => {
       res.json().then((res) => {
         console.log(res);
        if(res.key !== undefined) {
          window.location.href='/process-csv/?file_id='+fileItemId
        }

      })
         .catch(() =>{
          console.log(res.status)
      })

    })
}, 400);
});
