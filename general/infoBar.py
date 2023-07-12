from PyQt5.QtCore import Qt

from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, FluentIcon, InfoBarPosition

# 错误提示
def createErrorInfoBar(parent,title,content,position=InfoBarPosition.TOP):
    InfoBar.error(
        title=title,
        content=content,
        orient=Qt.Horizontal,
        isClosable=True,
        position=position,
        duration=-1,    # won't disappear automatically
        parent=parent
    )

def createInfoInfoBar(parent,title,content,position=InfoBarPosition.TOP_RIGHT):
    w = InfoBar(
        icon=InfoBarIcon.INFORMATION,
        title= title,
        content=content,
        orient=Qt.Vertical,    # vertical layout
        isClosable=True,
        position=position,
        duration=2000,
        parent=parent
    )
    w.addWidget(PushButton('Action'))
    w.show()

def createSuccessInfoBar(parent,title,content,position=InfoBarPosition.TOP):
    # convenient class mothod
    InfoBar.success(
        title=title,
        content=content,
        orient=Qt.Horizontal,
        isClosable=True,
        position=position,
        duration=2000,
        parent=parent
    )

def createWarningInfoBar(parent,title,content,position=InfoBarPosition.TOP_LEFT):
    InfoBar.warning(
        title=title,
        content=content,
        orient=Qt.Horizontal,
        isClosable=False,   # disable close button
        position=position,
        duration=2000,
        parent=parent
    )

def createCustomInfoBar(parent,title,content,position=InfoBarPosition.BOTTOM):
    w = InfoBar.new(
        icon=FluentIcon.GITHUB,
        title=title,
        content=content,
        orient=Qt.Horizontal,
        isClosable=True,
        position=position,
        duration=2000,
        parent=parent
    )
    w.setCustomBackgroundColor('white', '#202020')