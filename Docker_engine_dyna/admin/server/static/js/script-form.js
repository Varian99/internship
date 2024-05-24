function addListenerField() {
    var container = document.getElementById("listener-container");
    var listenerDiv = document.createElement("div");
    listenerDiv.className = "listener-field";

    //Dynamic input for name
    var inputName = document.createElement("input");
    inputName.type = "text";
    inputName.name = "listenersName[]";
    inputName.placeholder = "Listener container name";
    inputName.style= "width: 300px";
    inputName.className = "input";
    inputName.required = true;
    listenerDiv.appendChild(inputName);
    container.appendChild(listenerDiv);

    //Dynamic input for protocol
    var selectProto = document.createElement("select");
    selectProto.className = "input";
    selectProto.style.width = "250px";
    selectProto.name = "listenersProto[]";

    var defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Select a protocol";
    selectProto.appendChild(defaultOption);

    var options = ["Wifi", "Bluetooth", "Lorawan"];
    options.forEach(function(optionValue) {
        var option = document.createElement("option");
        option.value = optionValue.toLowerCase();
        option.textContent = optionValue;
        selectProto.appendChild(option);
    });
    selectProto.required = true;
    listenerDiv.appendChild(selectProto);
    container.appendChild(listenerDiv);

    //Dynamic input for port
    var inputProtoPort = document.createElement("input");
    inputProtoPort.type = "number";
    inputProtoPort.name = "listenersProtoPort[]";
    inputProtoPort.placeholder = "Port";
    inputProtoPort.style= "width: 200px";
    inputProtoPort.className = "input";
    inputProtoPort.required = true;
    listenerDiv.appendChild(inputProtoPort);
    container.appendChild(listenerDiv);
}
function removeListenerField() {
    var container = document.getElementById("listener-container");
    var listenerFields = container.getElementsByClassName("listener-field");

    if (listenerFields.length >= 1) {
        var lastlistenerField = listenerFields[listenerFields.length - 1];
        container.removeChild(lastlistenerField);
    }
}


function addTreatmentField() {
    var container = document.getElementById("treatment-container");
    var treatmentDiv = document.createElement("div");
    treatmentDiv.className = "treatment-field";

    //Dynamic input for name
    var inputName = document.createElement("input");
    inputName.type = "text";
    inputName.name = "treatmentsName[]";
    inputName.placeholder = "Treatment container name";
    inputName.style= "width: 300px";
    inputName.className = "input";
    inputName.required = true;
    treatmentDiv.appendChild(inputName);
    container.appendChild(treatmentDiv);
}
function removeTreatmentField() {
    var container = document.getElementById("treatment-container");
    var treatmentFields = container.getElementsByClassName("treatment-field");

    if (treatmentFields.length >= 1) {
        var lasttreatmentField = treatmentFields[treatmentFields.length - 1];
        container.removeChild(lasttreatmentField);
    }
}


function addSenderField() {
    var container = document.getElementById("sender-container");
    var senderDiv = document.createElement("div");
    senderDiv.className = "sender-field";

    //Dynamic input for name
    var inputName = document.createElement("input");
    inputName.type = "text";
    inputName.name = "sendersName[]";
    inputName.placeholder = "Sender container name";
    inputName.style= "width: 500px";
    inputName.className = "input";
    inputName.required = true;
    senderDiv.appendChild(inputName);
    container.appendChild(senderDiv);
}
function removeSenderField() {
    var container = document.getElementById("sender-container");
    var senderFields = container.getElementsByClassName("sender-field");

    if (senderFields.length >= 1) {
        var lastsenderField = senderFields[senderFields.length - 1];
        container.removeChild(lastsenderField);
    }
}