import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts

Rectangle {
  //anchors.fill: parent
  color: "grey"

TabBar {
  id: bar
  width: parent.width
  
  TabButton {
    text: "Source Code"
  }
  TabButton {
    text: "Module Items"
  }
}

StackLayout {
  id: root
  width: parent.width
  anchors.top: parent.top
  anchors.topMargin: 32
  currentIndex: bar.currentIndex


  Flickable {
    width: 200
    height: 200
    contentWidth: testtext.width
    contentHeight: testtext.height

    TextArea {
      id: testtext
      text: "TEsT TESTS SETSETSET"
    }

    ScrollBar.vertical: ScrollBar { }
  }

  Item {
    id: currentModuleName

    Rectangle {
        id: controlRoot

        property int count: 0

        Component.onCompleted: {
		createButton(0)
		createButton(1)
        }

	function createButton(xEx) {
            wonderButton.createObject(controlRoot, { width: 200, x: xEx * 208 + 16, text: "Count" + (xEx+1) })
            count += 1
        }

    }

    Component {
        id: wonderButton
        Button {
            text: "TEST"
        }
    }
  }
}
}
