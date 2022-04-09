// 获取应用实例
const app = getApp()
//需要在微信小程序平台网站上，开发-->开发管理-->开发设置-->服务器域名-->request合法域名处 填入 https://images.bemfa.com
Page({
  data: {
    uid:"4eacc0f55636840afb50e11a03a3b065",//用户密钥，巴法云控制台获取
    myTopic:"img",//图片上传的主题，图片云控制台创建
    num:1,      //获取的图片数量，可随意
    imgList:[], //存储图片地址和时间，用于前端展示
    picArr:[], //存储图片的地址，用于图片点击预览
    passwd:"",
  },
 
  onLoad:function () {
    var that = this
    that.getPicture()
    that.getPasswd()
    setInterval(function () {
      that.getPicture()
      that.getPasswd()
      console.log("轮播请求10秒触发一次");
    }, 10000)    //代表1秒钟发送一次请求
  },

  getPicture(){    //获取图片函数
    //api 接口详细说明见巴法云接入文档
    var that = this
    wx.request({
      url: 'https://images.bemfa.com/cloud/v1/get/', //获取图片接口，详见巴法云接入文档
      data: {
        uid: that.data.uid,       //uid字段
        topic: that.data.myTopic,//topic字段
        num:that.data.num        //num字段
      },
      header: {
        'content-type': "application/x-www-form-urlencoded"
      },
      success (res) {
         console.log(res)     //打印获取结果
         var imgArr = []      //定义空数组，用于临时存储图片地址和时间
         var arr = []         //定义空数组，用于临时存储图片地址
         for(var i = 0;i<res.data.data.length;i++){//遍历获取的结果数组
           var url = res.data.data[i].url          //提取图片地址
           var time = that.time(url.substring(url.lastIndexOf("-")+1,url.lastIndexOf(".")))//提取图时间
           imgArr.push({"url":url,"time":time})    //将存储图片地址和时间存入临时数组
           arr.push(url)                           //将存储图片地址存入临时数组
         }
         
         that.setData({     //把临时数组值复制给变量用于展示
           imgList:imgArr, //将临时存储图片地址和图片时间的数组赋值给用于图片预览的数组
           picArr:arr,    //将临时存储图片地址的数组赋值给用于图片预览的数组
         })
        console.log(that.data.imgList)   //打印赋值结果
      }
    })

  },
  getPasswd(){
    var that = this
    wx.request({
      url: 'http://192.168.1.146:8888/api',
      data: {
        passwd: 'password',
      },
      method:'POST',     // 默认 GET
      header: {
        'content-type': 'application/x-www-form-urlencoded'    // 默认值 application/json
      },
      success:res=> {
        console.log('---request success---')
        that.setData({
          passwd:res.data,
        })
        console.log(res.data)
      },
    })
  },
  clickImg(e){                      //点击预览函数
      console.log(e.currentTarget.dataset.index)    //打印数组索引值
      var nowIndex = e.currentTarget.dataset.index  //获取索引值
      wx.previewImage({           //图片预览接口
        current: this.data.picArr[nowIndex],//当前图片地址
        urls: this.data.picArr    //图片地址数组
      })
  },
  time(time) {                    //时间戳转时间函数
    var date = new Date(parseInt(time)*1000 + 8 * 3600 * 1000);
    return date.toJSON().substr(0, 19).replace('T', ' ');
  },

})
