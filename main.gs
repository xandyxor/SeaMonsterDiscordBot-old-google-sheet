var sheetName = 'money';
var headerRow = 1;
var table = Sheetfu.getTable(sheetName, headerRow);  

var sheetName2 = 'Trophy';
var table2 = Sheetfu.getTable(sheetName2, headerRow); 

var sheetName3 = 'log';
var table3 = Sheetfu.getTable(sheetName3, headerRow); 


week_day_dict = {
    0 : '星期一',
    1 : '星期二',
    2 : '星期三',
    3 : '星期四',
    4 : '星期五',
    5 : '星期六',
    6 : '星期日',
    7 : 'total',
}

trophy_dict = {
    0 : '金塊1000g',
    1 : '怪獸內丹',
    2 : '赫卡魯的突起',
    3 : '漂流追蹤者的外皮',
    4 : '幽冥鐵牙的顎骨',
    5 : '納恩薩克的角破片',
    6 : '坎迪杜姆的甲殼',
    7 : '古德蒙特海賊團的金幣',
}
function doPost(e) {
  var para = e.parameter, // 存放 Post 所有傳送的參數
      method = para.method;
  
  if (method == "write") {
    write_data(para);
  }
  if (method == "read") {
    JSONString = JSON.stringify(getallmoney(para.name))
    return ContentService.createTextOutput(JSONString).setMimeType(ContentService.MimeType.JSON);
  } 
  if (method == "write_Trophy"){
    updateTrophys(para);
  }
  if (method == "read_Trophy"){
    JSONString = JSON.stringify(getallTrophy(para.day))
    return ContentService.createTextOutput(JSONString).setMimeType(ContentService.MimeType.JSON);
  }
  if (method == "write_Trophy_raw"){
    updateTrophyraw(para);
  }
}

function doGet(e) {  
  var para = e.parameter, // 存放 Get 所有傳送的參數
      method = para.method;

  if (method == "write") {
    write_data(para);
  }
  if (method == "read") {
    JSONString = JSON.stringify(getallmoney(para.name))
    return ContentService.createTextOutput(JSONString).setMimeType(ContentService.MimeType.JSON);
  } 
  if (method == "write_Trophy"){
    updateTrophys(para);
  }
  if (method == "read_Trophy"){
    JSONString = JSON.stringify(getallTrophy(para.day))
    return ContentService.createTextOutput(JSONString).setMimeType(ContentService.MimeType.JSON);
  }
  if (method == "write_Trophy_raw"){
    updateTrophyraw(para);
  }
}


function write_data(para){
  Logger.log(para.name)
  Logger.log(para.day)
  Logger.log(para.money)
  updatemoney(para.name,para.day,para.money)  
}

function getallmoney(name){  
  allmoney = { "星期日":"0","星期一":"0","星期二":"0","星期三":"0","星期四":"0","星期五":"0","星期六":"0","total":"0"};  
  var item = table.select({"name": name}).first();  
  if (item == undefined){ // 查無此使用者(因此必須新增此使用者欄位
    Logger.log("undefined")
    addNewPerson(name);
    item = table.select({"name": name}).first(); //重新查詢
  }  
  for (var i = 0 ; i < 8 ; i++){ 
    var money_tmp = item.getFieldValue(week_day_dict[i]);
    
    if (!money_tmp ){
      allmoney[week_day_dict[i]] = 0
    }else{
      allmoney[week_day_dict[i]] = money_tmp
    }
  }
  //Logger.log(allmoney)
  return allmoney
}

//function getmoney(name,day){
//  var item = table.select({"name": name}).first();
//  var money = item.getFieldValue(day);
//  return item
//}

function updatemoney(name,day,money){
  var item = table.select({"name": name}).first();
  item.setFieldValue(day,money).commit();
}


function addNewPerson(name) {
    var newEmployee = {
        "name": name, 
    };
    table.add(newEmployee);
    table.commit()
}

function testfun(){
  //var item = table.select({"name": "Serapin"}).first();
//  Logger.log(updateTrophy("星期一","怪獸內丹",456))
//  Logger.log(getallTrophy("星期二"))
//  allTrophy = { "day":"星期一","金塊1000g":"10","怪獸內丹":"20","赫卡魯的突起":"30","漂流追蹤者的外皮":"0","幽冥鐵牙的顎骨":"0","納恩薩克的角破片":"70","坎迪杜姆的甲殼":"80","古德蒙特海賊團的金幣":"90"};
//  updateTrophys(allTrophy)
//  var item = table2.select({"day": "2018-08-14星期二"}).first();
//  var trophy_tmp = item.getFieldValue("金塊1000g"); 
//  var newLOG = {
//    "day": "2018-08-14星期二", 
//    "name": "Serapin", 
//    "金塊1000g": 0,
//    "怪獸內丹" :0,
//    "赫卡魯的突起":0,
//    "漂流追蹤者的外皮":0,
//    "幽冥鐵牙的顎骨":0,
//    "納恩薩克的角破片":0,
//    "坎迪杜姆的甲殼":0,
//    "古德蒙特海賊團的金幣":0
//  };
//  table3.add(newLOG);
//  table3.commit()

var item = table.select({"name": "Serapin"}).first();  
  if (item == undefined){ // 查無此使用者(因此必須新增此使用者欄位
    Logger.log("undefined")
  }
}


function updateTrophy(day,id,val){
  var item = table2.select({"day": day}).first();
  item.setFieldValue(id,val).commit();  
}

function updateTrophys(para){ 
  var item = table2.select({"day": para.day}).first();
  for (var i = 0 ; i < 8 ; i++){ 
    var trophy_tmp = para[trophy_dict[i]]; 
    item.setFieldValue(trophy_dict[i],trophy_tmp)
  }
  item.commit();
}

function updateTrophyraw(para){
  var newLOG = {
    "day": "2018-08-14星期二", 
    "name": "Serapin", 
    "金塊1000g": 0,
    "怪獸內丹" :0,
    "赫卡魯的突起":0,
    "漂流追蹤者的外皮":0,
    "幽冥鐵牙的顎骨":0,
    "納恩薩克的角破片":0,
    "坎迪杜姆的甲殼":0,
    "古德蒙特海賊團的金幣":0,
    "是否賣出":0
  };   
  for (var i = 0 ; i < 8 ; i++){ 
    var trophy_tmp = para[trophy_dict[i]]; 
    newLOG[trophy_dict[i]] = trophy_tmp
  }
  table3.add(newLOG);
  table3.commit();
}

function getallTrophy(day){
  allTrophy = { "金塊1000g":"0","怪獸內丹":"0","赫卡魯的突起":"0","漂流追蹤者的外皮":"0","幽冥鐵牙的顎骨":"0","納恩薩克的角破片":"0","坎迪杜姆的甲殼":"0","古德蒙特海賊團的金幣":"0"};  
  var item = table2.select({"day": day}).first();  
  if (item == undefined){ // 查無此日期(因此必須新增此日期欄位
    //Logger.log("undefined")
    addNewTrophy(day);
    item = table2.select({"day": day}).first(); //重新查詢
  }  
  for (var i = 0 ; i < 8 ; i++){     
    var trophy_tmp = item.getFieldValue(trophy_dict[i]);    
    if (!trophy_tmp ){
      allTrophy[trophy_dict[i]] = 0
    }else{
      allTrophy[trophy_dict[i]] = trophy_tmp
    }    
  }
  return allTrophy
}

function addNewTrophy(day) {
    var newEmployee = {
        "day": day, 
    };
    table2.add(newEmployee);
    table2.commit()
}

function check(){

}