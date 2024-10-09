// Function to get a form from a JSON object
function getFormFromJSON(object) {
    return buildFormFromObject(object);
}

// Function to build a form from the given object
function buildFormFromObject(object) {
    const form = document.createElement('form');
    const ul = document.createElement('ul');
    form.appendChild(ul);
    expandObject(object, ul);
    return form;
}

// Function to recursively expand the object
function expandObject(object, parent, parentKey = "") {
    Object.keys(object).forEach(key => {
        const elementId = `${parentKey}${key}`;
        const isNestedObject = (typeof (object[key]) === 'object') && (object[key] !== null);

        const newli = document.createElement('li');
        const span = document.createElement('span');
        const newul = document.createElement('ul');
        const li = buildListItem(key, object[key], elementId);
        const nestli = document.createElement('li');
        const nestspan = document.createElement('span');
        const nestul = document.createElement('ul');

        parent.appendChild(newli);
        newli.appendChild(span);
        span.appendChild(newul);
        newul.appendChild(li);
        li.appendChild(nestli);
        nestli.appendChild(nestspan);
        nestspan.appendChild(nestul);

        if (isNestedObject) {
            setAttr(span, { "class": "caret" });
            expandObject(object[key], nestul, `${elementId}.`);
        }

        if (parentKey === '') {
            parent.appendChild(li);
        }
    });
}

// Function to build a list item for the form
function buildListItem(key, value, elementId) {
    const li = document.createElement('li');
    const div = document.createElement('div');
    const label = document.createElement('label');
    const strong = document.createElement('strong');
    const input = document.createElement('input');

    li.appendChild(div);
    label.appendChild(strong);
    setAttr(label, { "for": elementId });
    setAttr(strong, { "innerHTML": key });

    let inputType = "input"; // Default input type

    switch (typeof value) {
        case 'string':
            setAttr(input, { "class": "form-control" });
            setAttr(input, { "class": "expand-textarea" });
        case 'number':
            setAttr(div, { "class": "form-group" });
            setAttr(input, { "class": "form-control" });
            div.appendChild(label);
            div.appendChild(input);
            break;
        case 'boolean':
            inputType = "select"; // Use select for boolean values
            const select = document.createElement('select');
            setAttr(div, { "class": "form-group" });
            setAttr(select, { "class": "form-control", "name": elementId });

            // Create options for true and false
            const trueOption = document.createElement('option');
            const falseOption = document.createElement('option');
            trueOption.text = "true";
            falseOption.text = "false";

            select.appendChild(trueOption);
            select.appendChild(falseOption);
            if (value) {
                trueOption.selected = true;
            } else {
                falseOption.selected = true;
            }

            div.appendChild(label);
            div.appendChild(select);
            break;
        case 'object':
            setAttr(input, { "type": "input" });
            if (value) {
                setAttr(input, { "hidden": "true" });
            } else {
                setAttr(input, { "readonly": "true" });
            }
            div.appendChild(label);
            div.appendChild(input);
            break;
    }

    setAttr(input, {
        "type": inputType,
        "name": elementId,
        "value": value
    });

    li.appendChild(div);
    return li;
}

// Function to generate a UUID
function uuid() {
    var dt = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (dt + Math.random() * 16) % 16 | 0;
        dt = Math.floor(dt / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}

// Function to set attributes on an element
function setAttr(element, attributes) {
    Object.keys(attributes).forEach(key => {
        if (key == "innerHTML") {
            element.innerHTML = attributes[key];
        } else {
            element.setAttribute(key, attributes[key]);
        }
    });
}

// Attach global functions to the window object for accessibility
window.getFormFromJSON = getFormFromJSON;
