
CREATE database mj;

-- 用户基本信息
CREATE TABLE user_info (
  u_id varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '', -- primary
  wx_openid varchar(255) DEFAULT NULL, -- wx_id
  wx_nickname varchar(500) DEFAULT NULL, -- wx昵称
  wx_sex int(10) DEFAULT NULL, -- 微信性别
  wx_country varchar(11) DEFAULT NULL, -- wx国家
  wx_headimgurl varchar(600) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL, -- wx头像
  sub_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 平台注册时间
  user_type int(2) DEFAULT 0, -- 用户类型 0:玩家 1:管理员 2:代理
  speed_type int(2) DEFAULT 0, -- 1神速 2快速 3快 4正常 5慢 6蜗牛 7龟速
  laipr_type int(2) DEFAULT 0, -- 赖皮等级:0正常，1：小赖，2：中赖，3：大赖，4：老赖
  escape_num int(2) DEFAULT 0, -- 逃跑次数
  break_num int(2) DEFAULT 0, -- 断线次数
  status varchar(2) DEFAULT 0, -- 0正常登录，1黑名单
  card_num int(2) DEFAULT 3, -- 新用户房卡数量
  offon_line varchar(2) DEFAULT 0, -- 0：不在线，1：在线
  PRIMARY KEY (u_id)
);



-- 房间信息
/*readme
owner 代表房间拥有者
*/
CREATE TABLE room_info(
  r_id varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '', -- primary房间编号，用户登录房间使用
  game_num int(2) DEFAULT NULL , -- 房间局数4 8
  sub_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP , -- 房卡创建时间
  east_id varchar(255) DEFAULT NULL , -- 房主 user_info.id
  south_id varchar(255) DEFAULT NULL , -- 下家
  west_id varchar(255) DEFAULT NULL , -- 下家
  north_id varchar(255) DEFAULT NULL ,-- 下家
  use_time timestamp , -- 房卡使用时间
  user_list varchar(100) DEFAULT "east_id:,south_id:,west_id:,north_id:",
  black_users varchar(1000) DEFAULT NULL , -- 黑名单
  room_style VARCHAR(50) DEFAULT NULL , -- 1：4局牌，2：8局牌，3：下鱼2条，4：下鱼5条，5：下鱼8条，6：不要风牌，7：自能自摸胡
  room_status int(2) DEFAULT 0,-- 0：房间未使用;1：房间开始游戏;2：房间游戏结束
  PRIMARY KEY (r_id)
);



-- 用户被房间踢出次数
/*readme
用户被踢出3次后达到被踢上线，讲不能进入该房间，kick_num 最大值为3
 */
CREATE TABLE room_black_list(
  rb_id varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '', -- primary
  r_id varchar(25) NOT NULL ,
  u_id varchar(255) NOT NULL ,
  kick_num int(2) DEFAULT 0,
  PRIMARY KEY (rb_id)
);


-- 房间各局游戏结果
/* readme
  依据总成绩计算
 */
CREATE TABLE game_result (
  gr_id varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '', -- primary
  r_id varchar(25) NOT NULL, -- 房间编号
  game_num int(2) DEFAULT NULL , -- 房间牌局
  now_num int(2) DEFAULT NULL , -- 当前牌局
  east_id varchar(255) DEFAULT NULL , -- 庄家id
  east_zm int(2) DEFAULT NULL , -- 自摸次数
  east_jp int(2) DEFAULT NULL , -- 接炮次数
  east_dp int(2) DEFAULT NULL , -- 点炮次数
  east_xy int(2) DEFAULT NULL , -- 下鱼条数
  east_mg int(2) DEFAULT NULL , -- 明杠条数
  east_ag int(2) DEFAULT NULL , -- 暗杠条数
  east_cj int(3) DEFAULT NULL , -- 总成绩
  east_wl int(2) DEFAULT NULL , -- 0进行中1赢2输3流局
  south_id varchar(255) DEFAULT NULL , -- 玩家id
  south_zm int(2) DEFAULT NULL , -- 自摸次数
  south_jp int(2) DEFAULT NULL , -- 接炮次数
  south_dp int(2) DEFAULT NULL , -- 点炮次数
  south_xy int(2) DEFAULT NULL , -- 下鱼条数
  south_mg int(2) DEFAULT NULL , -- 明杠条数
  south_ag int(2) DEFAULT NULL , -- 暗杠条数
  south_cj int(3) DEFAULT NULL , -- 总成绩
  south_wl int(2) DEFAULT NULL , -- 0输1赢
  west_id varchar(255) DEFAULT NULL , -- 玩家id
  west_zm int(2) DEFAULT NULL , -- 自摸次数
  west_jp int(2) DEFAULT NULL , -- 接炮次数
  west_dp int(2) DEFAULT NULL , -- 点炮次数
  west_xy int(2) DEFAULT NULL , -- 下鱼条数
  west_mg int(2) DEFAULT NULL , -- 明杠条数
  west_ag int(2) DEFAULT NULL , -- 暗杠条数
  west_cj int(3) DEFAULT NULL , -- 总成绩
  west_wl int(2) DEFAULT NULL , -- 0输1赢
  north_id varchar(255) DEFAULT NULL , -- 玩家id
  north_zm int(2) DEFAULT NULL , -- 自摸次数
  north_jp int(2) DEFAULT NULL , -- 接炮次数
  north_dp int(2) DEFAULT NULL , -- 点炮次数
  north_xy int(2) DEFAULT NULL , -- 下鱼条数
  north_mg int(2) DEFAULT NULL , -- 明杠条数
  north_ag int(2) DEFAULT NULL , -- 暗杠条数
  north_cj int(3) DEFAULT NULL , -- 总成绩
  north_wl int(2) DEFAULT NULL , -- 0输1赢
  PRIMARY KEY (gr_id)
);

-- 游戏过房间状态记录
/* readme
  可根据
 */
CREATE TABLE game_info (
  gi_id         VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '', -- primary
  r_id          VARCHAR(25) NOT NULL, -- 房间编号
  g_num         int(2) DEFAULT 8, -- 房间牌局
  east_id       VARCHAR(255)  NOT NULL , -- A家id 房主
  east_mj       VARCHAR(50)  NOT NULL , -- A家牌
  east_mg       VARCHAR(255) DEFAULT NULL ,
  east_ag       varchar(255) DEFAULT NULL ,
  east_mf       int(2) DEFAULT 0, -- 明杠分数
  east_af       int(2) DEFAULT 0, -- 暗杠分数
  east_dg       int(2) DEFAULT 0, -- 点杠分数
  east_p        VARCHAR(255) DEFAULT NULL ,
  east_j        VARCHAR(50) DEFAULT NULL , -- 金牌
  east_act      varchar(100) DEFAULT NULL , -- 0：无动作(过)；1：抓牌；2：出牌；3：碰；4：明杠；5：暗杠；6：胡; 7：接炮；8：点炮；9：申请终止牌局；10：同意终止牌局；11：不同意终止牌局
  east_doact    varchar(10) DEFAULT NULL , -- 0：无动作；1：抓牌；2：出牌；3：碰；4：明杠；5：暗杠；6：胡; 7：接炮；8：点炮；9：申请终止牌局；10：同意终止牌局；11：不同意终止牌局；
  south_id      varchar(255)  NOT NULL , -- B家id
  south_mj      VARCHAR(50)  NOT NULL , -- B家牌
  south_mg      varchar(255) DEFAULT NULL ,
  south_ag      varchar(255) DEFAULT NULL ,
  south_mf       int(2) DEFAULT 0, -- 明杠分数
  south_af       int(2) DEFAULT 0, -- 暗杠分数
  south_dg       int(2) DEFAULT 0, -- 点杠分数
  south_p       VARCHAR(255) DEFAULT NULL ,
  south_j        VARCHAR(50) DEFAULT NULL , -- 金牌
  south_act     varchar(255) DEFAULT NULL ,
  south_doact   varchar(20) DEFAULT NULL ,
  west_id       varchar(255)  NOT NULL , -- C家id
  west_mj       VARCHAR(50)  NOT NULL , -- C家牌
  west_mg       varchar(255) DEFAULT NULL ,
  west_ag       varchar(255) DEFAULT NULL ,
  west_mf       int(2) DEFAULT 0, -- 明杠分数
  west_af       int(2) DEFAULT 0, -- 暗杠分数
  west_dg       int(2) DEFAULT 0, -- 点杠分数
  west_p        VARCHAR(255) DEFAULT NULL ,
  west_j        VARCHAR(50) DEFAULT NULL , -- 金牌
  west_act      varchar(100) DEFAULT NULL ,
  west_doact   varchar(20) DEFAULT NULL ,
  north_id      varchar(255)  NOT NULL , -- D家id
  north_mj      VARCHAR(50)  NOT NULL , -- D家牌
  north_mg      varchar(255) DEFAULT NULL ,
  north_ag      varchar(255) DEFAULT NULL ,
  north_mf       int(2) DEFAULT 0, -- 明杠分数
  north_af       int(2) DEFAULT 0, -- 暗杠分数
  north_dg       int(2) DEFAULT 0, -- 点杠分数
  north_p       VARCHAR(255) DEFAULT NULL ,
  north_j        VARCHAR(50) DEFAULT NULL , -- 金牌
  north_act     varchar(100) DEFAULT NULL ,
  north_doact   varchar(20) DEFAULT NULL ,
  pointer       VARCHAR (255) DEFAULT '' , -- 手牌标示 e:u_id,s:u_id,w:u_id,n:u_id
  shou_pai      VARCHAR(10) DEFAULT '', -- 牌 0:无牌
  old_mj        VARCHAR (500) DEFAULT NULL , -- 牌桌上打出的牌
  now_mj        VARCHAR (10)  NOT NULL , -- 当前玩家打出的牌(牌桌上的牌) u_id:pai
  sub_time      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 时间戳
  time_consume  int(100) DEFAULT 0 , -- 耗时
  data_type     int(1) DEFAULT 0, -- 数据类型，1：帮助回放，0对回放无用
  room_style VARCHAR(50) DEFAULT NULL , -- 1：4局牌，2：8局牌，3：下鱼2条，4：下鱼5条，5：下鱼8条，6：不要风牌，7：只能自摸胡，格式：1,3,7
  PRIMARY KEY (gi_id)
);


--房间牌山
/* readme
  房间牌山记录
 */
CREATE TABLE room_mj_info(
  mj_id VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '', -- primary
  r_id varchar(25) NOT NULL, -- 房间id
  paishan varchar(800) NOT NULL, -- 房间id
  g_num int(2) NOT NULL , -- 牌局
  ga_num int(10) NOT NULL , -- 当前牌局杠次数
  bao_index int(2) NOT NULL , -- 1-6随机数
  sub_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 时间戳
  PRIMARY key (mj_id)
);


-- init database
drop table game_info;
drop table game_result;
drop table room_black_list;
drop table room_info;
drop table room_mj_info;
drop table user_info;

truncate table game_info;
truncate table game_result;
truncate table room_black_list;
truncate table room_info;
truncate table room_mj_info;
truncate table user_info;


