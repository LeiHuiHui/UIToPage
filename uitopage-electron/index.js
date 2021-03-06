const {app, BrowserWindow, Menu} = require('electron')

// 保持对window对象的全局引用，如果不这么做的话，当JavaScript对象被
// 垃圾回收的时候，window对象将会自动的关闭
let win

const template = [
    {
        label:'文件',
        submenu:[
            {
                label:'导入工程文件',
                accelerator: 'CmdOrCtrl+I',
                click: function(menuItem,browserWindow){console.log("hello");}
            },
            {
                label:'导出工程文件',
                accelerator: 'CmdOrCtrl+E',
            },
            {
                label:'下载页面',
                accelerator: 'CmdOrCtrl+S',
            }
        ]
    },
    {
        label:'编辑',
        submenu:[
            {
                label:'上一步',
                accelerator: 'CmdOrCtrl+Z',
            },
            {
                label:'下一步',
                accelerator: 'Shift+CmdOrCtrl+Z',
            },
            {
                label:'清空',
                accelerator: 'CmdOrCtrl+D',
            }
        ]
    },
    {
        label:'视图',
        submenu:[
            {
                label:'预览',
                accelerator: 'CmdOrCtrl+P',
            },
            {
                label:'退出预览',
                accelerator: 'Shift+CmdOrCtrl+P',
            }
        ]
    },
    {
        label:'AI识别',
        submenu:[
            {
                label:'导入UI截图',
                accelerator: 'CmdOrCtrl+U',
            }
        ]
    }

]

function createWindow() {
    // 创建浏览器窗口
    let win = new BrowserWindow({
        width:800,
        height:600,
        webPreference:{
            nodeIntegration:true
        }
    })

    // 加载index.html文件
    win.loadFile('index.html')

    // 打开开发者工具
    // win.webContents.openDevTools()

    // 当 window 被关闭，这个事件会被触发。
    win.on('closed', () => {
        // 取消引用 window 对象，如果你的应用支持多窗口的话，
        // 通常会把多个 window 对象存放在一个数组里面，
        // 与此同时，你应该删除相应的元素。
        win = null
    })
}

// Electron 会在初始化后并准备
// 创建浏览器窗口时，调用这个函数。
// 部分 API 在 ready 事件触发后才能使用。
// app.on('ready',createWindow)
app.on('ready',function(){
    const menu = Menu.buildFromTemplate(template)
    Menu.setApplicationMenu(null) // 设置菜单部分
    createWindow()
})


// 当全部窗口关闭时退出。
app.on('window-all-closed', () => {
    // 在 macOS 上，除非用户用 Cmd + Q 确定地退出，
    // 否则绝大部分应用及其菜单栏会保持激活。
    if (process.platform !== 'darwin') {
      app.quit()
    }
  })

app.on('activate', () => {
// 在macOS上，当单击dock图标并且没有其他窗口打开时，
// 通常在应用程序中重新创建一个窗口。
if (win === null) {
    createWindow()
}
})

// 在这个文件中，你可以续写应用剩下主进程代码。
// 也可以拆分成几个文件，然后用 require 导入。