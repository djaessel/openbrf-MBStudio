import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 2.0

Rectangle {
    anchors.fill: parent
    color: "red"

    Button {
        id: addButton
	anchors.centerIn: parent
        text: "TEST"
        flat: false
	palette {
            button: "black"
	    buttonText: "green"
        }
        onClicked: {
            console.log("HELP ME")
            addButton.text = "HELP ME"
        }
    }
}
