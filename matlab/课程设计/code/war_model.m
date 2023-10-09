function varargout = war_model(varargin)
%WAR_MODEL MATLAB code file for war_model.fig
%      WAR_MODEL, by itself, creates a new WAR_MODEL or raises the existing
%      singleton*.
%
%      H = WAR_MODEL returns the handle to a new WAR_MODEL or the handle to
%      the existing singleton*. 
%
%      WAR_MODEL('Property','Value',...) creates a new WAR_MODEL using the
%      given property value pairs. Unrecognized properties are passed via
%      varargin to war_model_OpeningFcn.  This calling syntax produces a
%      warning when there is an existing singleton*.
%
%      WAR_MODEL('CALLBACK') and WAR_MODEL('CALLBACK',hObject,...) call the
%      local function named CALLBACK in WAR_MODEL.M with the given input
%      arguments.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help war_model

% Last Modified by GUIDE v2.5 02-Feb-2023 18:20:04

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @war_model_OpeningFcn, ...
                   'gui_OutputFcn',  @war_model_OutputFcn, ...
                   'gui_LayoutFcn',  [], ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
   gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT
end

% --- Executes just before war_model is made visible.
function war_model_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   unrecognized PropertyName/PropertyValue pairs from the
%            command line (see VARARGIN)

% Choose default command line output for war_model
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);
%% 参数初始设置
set(handles.now,'string','0')%初始时间为0
set(handles.type,'value',1);%默认设置为正规战
handles.wartype = 1;
set(handles.x0,'string',1000);%甲方初始人数为100人
handles.x_0 = 1000;
set(handles.alpha,'string',0.01);%甲方非战斗减员率
handles.a = 0.01;
set(handles.rx,'string',5);%甲方单个士兵射击率
handles.r_x = 5;
set(handles.px,'string',0.3);%甲方单射击命中率
handles.p_x = 0.3;
set(handles.sx,'string',0.5);%甲方有效活动面积所占比例
handles.s_x = 0.5;
set(handles.y0,'string',1000);%乙方初始人数为100人
handles.y_0 = 1000;
set(handles.beta,'string',0.01);%乙方非战斗减员率
handles.b = 0.01;
set(handles.ry,'string',4);%乙方单个士兵射击率
handles.r_y = 4;
set(handles.py,'string',0.3);%乙方单射击命中率
handles.p_y = 0.3;
set(handles.sy,'string',0.5);%乙方有效活动面积所占比例
handles.s_y = 0.5;
set(handles.dt,'string',1);%等间隔仿真步长初始化为1
handles.step_dt = 1;
set(handles.time,'string',5);%设置总仿真时长限制
handles.timeall = 5;
set(handles.x_add,'string',0);%设置甲方增加兵力人数
handles.xadd = 0;
set(handles.y_add,'string',0);%设置乙方增加兵力人数
handles.yadd = 0;
handles.flag_add = 0;%是否增兵标志 如果为1 则为增兵 否则为不增兵
guidata(hObject, handles);
%% 坐标轴初始化设置
%axes1为结果绘制窗口，初始化为显示刻度，坐标轴设置为0到无穷
set(handles.axes1,'XGrid','on');set(handles.axes1,'XLim',[0 inf]);
set(handles.axes1,'YGrid','on');set(handles.axes1,'YLim',[0 inf]);
% UIWAIT makes war_model wait for user response (see UIRESUME)
% uiwait(handles.figure1);
end


% --- Outputs from this function are returned to the command line.
function varargout = war_model_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;
end

% --- Executes during object creation, after setting all properties.
function edit2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
end

% --- Executes during object creation, after setting all properties.
function time_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
end

% 确定战争类型  1对应正规战 2对应游击战 3对应混合战
function type_Callback(hObject, eventdata, handles)
% hObject    handle to type (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns type contents as cell array
%        contents{get(hObject,'Value')} returns selected item from type
wartype = get(hObject,'value'); %战争类型 1对应正规战 2对应游击战 3对应混合战
handles.wartype = wartype;
guidata(hObject,handles);
end

% --- Executes during object creation, after setting all properties.
function type_CreateFcn(hObject, eventdata, handles)
% hObject    handle to type (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
end

% 关闭仿真图窗，退出界面
function exit_Callback(hObject, eventdata, handles)
    close(gcbf);%关闭当前图窗
end

% 修改dt 一次迭代步长
function dt_Callback(hObject, eventdata, handles)
% hObject    handle to dt (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
dt = str2double(get(hObject,'String'));
handles.step_dt = dt;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of dt as text
%        str2double(get(hObject,'String')) returns contents of dt as a double
end

% --- Executes during object creation, after setting all properties.
function dt_CreateFcn(hObject, eventdata, handles)
% hObject    handle to dt (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
end

% --- Executes on mouse press over axes background.
function axes1_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to axes1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
end

% --- Executes during object creation, after setting all properties.
function x_CreateFcn(hObject, eventdata, handles)
% hObject    handle to x (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
end

%对x_0(甲方初始兵力)进行设置
function x0_Callback(hObject, eventdata, handles)
% hObject    handle to x0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
x0 = str2double(get(hObject,'string'));
handles.x_0 = x0;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of x0 as text
%        str2double(get(hObject,'String')) returns contents of x0 as a double
end

% 对alpha（甲方非战斗减员率）进行设置
function alpha_Callback(hObject, eventdata, handles)
% hObject    handle to alpha (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
alpha = str2double(get(hObject,'String'));
handles.a = alpha;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of alpha as text
%        str2double(get(hObject,'String')) returns contents of alpha as a double
end

%修改甲方的单士兵射击率
function rx_Callback(hObject, eventdata, handles)
% hObject    handle to rx (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
rx = str2double(get(hObject,'String'));
handles.r_x = rx;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of rx as text
%        str2double(get(hObject,'String')) returns contents of rx as a double
end

%修改甲方的单射击命中率
function px_Callback(hObject, eventdata, handles)
% hObject    handle to px (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
px = str2double(get(hObject,'String'));
handles.p_x = px;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of px as text
%        str2double(get(hObject,'String')) returns contents of px as a double
end

%修改甲方的有效活动面积比率
function sx_Callback(hObject, eventdata, handles)
% hObject    handle to sx (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
sx = str2double(get(hObject,'String'));
handles.s_x = sx;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of sx as text
%        str2double(get(hObject,'String')) returns contents of sx as a double
end

%修改乙方的初始兵力个数
function y0_Callback(hObject, eventdata, handles)
% hObject    handle to y0 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
y0 =  str2double(get(hObject,'String'));
handles.y_0 =y0;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of y0 as text
%        str2double(get(hObject,'String')) returns contents of y0 as a double
end

% 修改乙方非战斗减员率b
function beta_Callback(hObject, eventdata, handles)
% hObject    handle to beta (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
b = str2double(get(hObject,'String'));
handles.b = b;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of beta as text
%        str2double(get(hObject,'String')) returns contents of beta as a double
end

% 修改乙方单士兵射击率
function ry_Callback(hObject, eventdata, handles)
% hObject    handle to ry (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
ry = str2double(get(hObject,'String'));
handles.r_y = ry;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of ry as text
%        str2double(get(hObject,'String')) returns contents of ry as a double
end

%修改乙方单射击命中率
function py_Callback(hObject, eventdata, handles)
% hObject    handle to py (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
py =  str2double(get(hObject,'String'));
handles.p_y = py;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of py as text
%        str2double(get(hObject,'String')) returns contents of py as a double
end

%修改乙方有效活动面积所占比例
function sy_Callback(hObject, eventdata, handles)
% hObject    handle to sy (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
sy = str2double(get(hObject,'String'));
handles.s_y = sy;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of sy as text
%        str2double(get(hObject,'String')) returns contents of sy as a double
end

%设置总仿真时间
function time_Callback(hObject, eventdata, handles)
% hObject    handle to now (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
time =  str2double(get(hObject,'String'));
handles.timeall =time;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of now as text
%        str2double(get(hObject,'String')) returns contents of now as a double
end

%获得甲方军队增加兵力数目
function x_add_Callback(hObject, eventdata, handles)
% hObject    handle to x_add (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
xadd = str2double((get(hObject,'String')));
handles.xadd = xadd;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of x_add as text
%        str2double(get(hObject,'String')) returns contents of x_add as a double
end

%获得乙方军队增加兵力数目
function y_add_Callback(hObject, eventdata, handles)
% hObject    handle to y_add (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
yadd = str2double((get(hObject,'String')));
handles.yadd = yadd;
guidata(hObject,handles);
% Hints: get(hObject,'String') returns contents of y_add as text
%        str2double(get(hObject,'String')) returns contents of y_add as a double
end


% 是否增加兵力（援助）
function add_Callback(hObject, eventdata, handles)
% hObject    handle to add (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.flag_add = 1;%是否增兵标志 如果为1 则为增兵 否则为不增兵
guidata(hObject, handles);
end
  
% --- Executes during object creation, after setting all properties.
function begin_CreateFcn(hObject, eventdata, handles)
% hObject    handle to begin (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
end

% --- Executes during object deletion, before destroying properties.
function begin_DeleteFcn(hObject, eventdata, handles)
% hObject    handle to begin (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
end

% 存储所绘制的图像
function save_Callback(hObject, eventdata, handles)
% hObject    handle to save (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
newpicture=figure('visible','off'); %新建一个不可见的figure
new_axes=copyobj(handles.axes1,newpicture); %axes1是GUI界面内要保存图线的Tag，将其copy到不可见的figure中
set(new_axes,'Units','normalized','Position',[0.1 0.1 0.8 0.8]);%将图线缩放
[filename pathname] = uiputfile('*.jpg','保存图像');
if filename == 0
    return;
else
    file = strcat(pathname,filename);
    print(newpicture,'-djpeg',file)
    fig = uifigure;
    message = {'已成功保存图片','可以继续进行模拟'};
    uialert(fig,message,'保存图像','Icon','success');
end
end
% --- Executes during object deletion, before destroying properties.
function begin_Callback(hObject, eventdata, handles)
% hObject    handle to begin (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%% 开始仿真 
%% 仿真参数初始化
%将handles中存储的参数读出
now = 0;dt = handles.step_dt; %初始仿真时间、时间间隔
t_list =[];%用于存储记录时间序列，方便后续绘图
time = handles.timeall;%仿真总时长
wartype = handles.wartype;%战争类型，决定仿真过程中的具体模型建立
x0 = handles.x_0;a = handles.a;%读出甲军队的相关参数
if(x0<=0)
    set(handles.flag,'string','甲方军队不能为负数');%报错信息
    pause(1);
    set(handles.x0,'string','');%删除不合法参数 重新输入
    set(handles.flag,'string','仿真未开始');%修改仿真状态为仿真未开始
end
x = x0;%甲军队的最初数目 初始化为x0
x_list = [];%用于存储甲军队兵力数目
rx = handles.r_x;%甲方军队的单士兵射击率
px = handles.p_x;%甲方军队的单射击命中率
sx = handles.s_x;%甲方有效活动面积
y0 = handles.y_0;b = handles.b;%读出乙军队的相关参数
y = y0;%乙军队的最初数目 初始化为y0
if(y0<=0)
    set(handles.flag,   'string','乙方军队不能为负数');%报错信息
    pause(1);
    set(handles.y0,'string','');%删除不合法参数 重新输入
    set(handles.flag,'string','仿真未开始');%修改仿真状态为仿真未开始
end
y_list = [];%用于存储乙军队的兵力数目
ry = handles.r_y;%乙方军队的单士兵射击率
py = handles.p_y;%乙方军队的单射击命中率
sy = handles.s_y;%乙方有效活动面积
if(x0>0 & y0>0)%验证初始人数是否符合要求 甲方乙方的初始兵力不能为负数
%% 开始仿真
switch wartype
   %%  正规战
    case 1 
       %进行迭代仿真
      set(handles.xwinflag,'string',' ');%清除甲方的士兵数目
      set(handles.ywinflag,'string',' ');%清除乙方的士兵数目
      for now = 0 : dt : time-dt  %根据仿真步长和仿真时间总限制进行循环
         set(handles.flag,'string','仿真进行中...请稍后');%修改仿真状态为仿真进行时
         set(handles.now,'string',now);%修改仿真时间显示
         tspan=[now  now+dt];%ode求解时间间隔 利用ode进行迭代求解
         [ttemp,ytemp] = ode45(@(t,y) odefun1(t,y,rx,px,ry,py,a,b),tspan,[x;y]);%在等间隔的时间范围时间点tspan之间进行ode求解（变长求解）
         for j = 1:1: length(ttemp)%变长求解的每一个时间点都记录下来
            now = ttemp(j);%变长求解的时间点
            x = floor(ytemp(j,1)); y = floor(ytemp(j,2));%甲方和乙方人数取整（向下取整）
            if (x>=0 & y>=0)%人数不能为负数，出现有一方人数为0则退出仿真
                t_list = [t_list,now];%记录仿真的时间点，方便后续作图
                x_list = [x_list,x];%记录甲方人数
                y_list = [y_list,y];%记录乙方人数
                set(handles.now,'string',now);%显示仿真的时间点
                set(handles.xnum,'string',x);%显示甲方的人数
                set(handles.ynum,'string',y);%显示乙方的人数
                axes(handles.axes1);%设置作图的句柄 绘制人数-时间变化图
                plot(t_list,x_list,'-b.',t_list,y_list,'-r.');%进行人数图的绘制
                legend('甲方','乙方');%标记线
                xlabel('仿真时间t');ylabel('士兵数目');%标记图
                title('战争士兵数仿真曲线')
                axes(handles.axes3);%设置作图的句柄 动态仿真图
                cla reset;%清空上次的动态仿真图
                box on;set(handles.axes3,'xtick',[]);
                set(handles.axes3,'ytick',[]);
                x_idx = zeros([x,2]);y_idx =  zeros([y,2]);%随机产生甲乙俩军队的士兵坐标
                x_idx(:,1) =0 +(sx -0).*rand(x ,1);x_idx(:,2) = 0 +(1 -0).*rand(x ,1);
                y_idx(:,1) =sx +(sy-0).*rand(y ,1); y_idx(:,2) =0 +(1-0).*rand(y ,1);
                scatter(x_idx(:,1),x_idx(:,2),'.b');%绘制散点图，甲方军队
                hold on;
                scatter(y_idx(:,1),y_idx(:,2),'.r');%绘制散点图，乙方军队
                legend('甲方军队','乙方军队');
                xlabel('战场区域');
                title('动态过程仿真');
                if(x*y==0)%如果出现某方士兵数目为0 退出仿真
                    break;
                end
            elseif(x*y<=0)%如果出现某方士兵数目为负数 退出仿真
                break;
            end
         end
         if(x*y<=0)%如果出现某方士兵数目为负数 退出仿真
             break;
         end
      end
       if(x>y)%甲方胜利 乙方失败
          set(handles.xwinflag,'string','胜利,可以乘胜追击');
          set(handles.ywinflag,'string','失败,需要增加兵力，提高军队作战能力');
      elseif(x<y)%甲方失败 乙方胜利
          set(handles.ywinflag,'string','胜利,可以乘胜追击');
          set(handles.xwinflag,'string','失败,需要增加兵力，提高军队作战能力');
      elseif(x==y)%双方战平
          set(handles.ywinflag,'string','双方战为平局');
          set(handles.xwinflag,'string','双方战为平局');
       end
       set(handles.flag,'string','仿真结束');%修改仿真状态 结束仿真

        %%  游击战
    case 2 
       %进行迭代仿真
      set(handles.xwinflag,'string',' ');%清除甲方的士兵数目
      set(handles.ywinflag,'string',' ');%清除乙方的士兵数目
      for now = 0 : dt : time-dt %根据仿真步长和仿真时间总限制进行循环
         set(handles.flag,'string','仿真进行中...请稍后');%修改仿真状态为仿真进行时
         set(handles.now,'string',now);%修改仿真时间显示
         tspan=[now  now+dt];%ode求解时间间隔 利用ode进行迭代求解
         [ttemp,ytemp] = ode45(@(t,y) odefun2(t,y,rx,sx,ry,sy,a,b),tspan,[x;y]);%在等间隔的时间范围时间点tspan之间进行ode求解（变长求解）
         for j = 1:1: length(ttemp)%变长求解的每一个时间点都记录下来
            now = ttemp(j);%变长求解的时间点
            x = floor(ytemp(j,1)); y = floor(ytemp(j,2));%甲方和乙方人数取整（向下取整）
            if (x>=0 & y>=0)%人数不能为负数，出现有一方人数为0则退出仿真
                t_list = [t_list,now];%记录仿真的时间点，方便后续作图
                x_list = [x_list,x];%记录甲方人数
                y_list = [y_list,y];%记录乙方人数
                set(handles.now,'string',now);%显示仿真的时间点
                set(handles.xnum,'string',x);%显示甲方的人数
                set(handles.ynum,'string',y);%显示乙方的人数
                axes(handles.axes1);%设置作图的句柄 绘制人数-时间变化图
                plot(t_list,x_list,'-b.',t_list,y_list,'-r.');%进行人数图的绘制
                legend('甲方','乙方');%标记线
                xlabel('仿真时间t');ylabel('士兵数目');
                title('战争士兵数仿真曲线')
                axes(handles.axes3);%设置作图的句柄 动态仿真图
                cla reset;%清空上次的动态仿真图
                box on;set(handles.axes3,'xtick',[]);
                set(handles.axes3,'ytick',[]);
                x_idx = zeros([x,2]);y_idx =  zeros([y,2]);%随机产生甲乙俩军队的士兵坐标
                x_idx(:,1) =0 +(sx -0).*rand(x ,1);x_idx(:,2) = 0 +(1 -0).*rand(x ,1);
                y_idx(:,1) =sx +(sy-0).*rand(y ,1); y_idx(:,2) =0 +(1-0).*rand(y ,1);
                scatter(x_idx(:,1),x_idx(:,2),'.b');%绘制散点图，甲方军队
                hold on;
                scatter(y_idx(:,1),y_idx(:,2),'.r');%绘制散点图，乙方军队
                legend('甲方军队','乙方军队');
                xlabel('战场宽');ylabel('战场高');
                title('动态过程仿真');
                if(x*y==0)%如果出现某方士兵数目为0 退出仿真
                    break;
                end
            elseif(x*y<=0)%如果出现某方士兵数目为负数 退出仿真
                break;
            end
         end
         if(x*y<=0)%如果出现某方士兵数目为负数 退出仿真
             break;
         end
      end
       if(x>y)%甲方胜利 乙方失败
          set(handles.xwinflag,'string','胜利,可以乘胜追击');
          set(handles.ywinflag,'string','失败,需要增加兵力，提高军队作战能力');
      elseif(x<y)%甲方失败 乙方胜利
          set(handles.ywinflag,'string','胜利,可以乘胜追击');
          set(handles.xwinflag,'string','失败,需要增加兵力，提高军队作战能力');
      elseif(x==y)%双方战平
          set(handles.ywinflag,'string','双方战为平局');
          set(handles.xwinflag,'string','双方战为平局');
       end
       set(handles.flag,'string','仿真结束');%修改仿真状态 结束仿真

    %%  混合战
    case 3 
       %进行迭代仿真
      set(handles.xwinflag,'string',' ');%清除甲方的士兵数目
      set(handles.ywinflag,'string',' ');%清除乙方的士兵数目
      for now = 0 : dt : time-dt %根据仿真步长和仿真时间总限制进行循环
         set(handles.flag,'string','仿真进行中...请稍后');%修改仿真状态为仿真进行时
         set(handles.now,'string',now);%修改仿真时间显示
         tspan=[now  now+dt];%ode求解时间间隔 利用ode进行迭代求解
         [ttemp,ytemp] = ode45(@(t,y) odefun3(t,y,rx,sx,ry,sy,px,a,b),tspan,[x;y]);%在等间隔的时间范围时间点tspan之间进行ode求解（变长求解）
         for j = 1:1: length(ttemp)%变长求解的每一个时间点都记录下来
            now = ttemp(j);%变长求解的时间点
            x = floor(ytemp(j,1)); y = floor(ytemp(j,2));%甲方和乙方人数取整（向下取整）
            if (x>=0 & y>=0)%人数不能为负数，出现有一方人数为0则退出仿真
                t_list = [t_list,now];%记录仿真的时间点，方便后续作图
                x_list = [x_list,x];%记录甲方人数
                y_list = [y_list,y];%记录乙方人数
                set(handles.now,'string',now);%显示仿真的时间点
                set(handles.xnum,'string',x);%显示甲方的人数
                set(handles.ynum,'string',y);%显示乙方的人数
                axes(handles.axes1);%设置作图的句柄 绘制人数-时间变化图
                plot(t_list,x_list,'-b.',t_list,y_list,'-r.');%进行人数图的绘制
                legend('甲方','乙方');%标记线
                xlabel('仿真时间t');ylabel('士兵数目');
                title('战争士兵数仿真曲线')
                axes(handles.axes3);%设置作图的句柄 动态仿真图
                cla reset;%清空上次的动态仿真图
                box on;set(handles.axes3,'xtick',[]);
                set(handles.axes3,'ytick',[]);
                x_idx = zeros([x,2]);y_idx =  zeros([y,2]);%随机产生甲乙俩军队的士兵坐标
                x_idx(:,1) =0 +(sx -0).*rand(x ,1);x_idx(:,2) = 0 +(1 -0).*rand(x ,1);
                y_idx(:,1) =sx +(sy-0).*rand(y ,1); y_idx(:,2) =0 +(1-0).*rand(y ,1);
                scatter(x_idx(:,1),x_idx(:,2),'.b');%绘制散点图，甲方军队
                hold on;
                scatter(y_idx(:,1),y_idx(:,2),'.r');%绘制散点图，乙方军队
                legend('甲方军队','乙方军队');
                xlabel('战场宽');ylabel('战场高');
                title('动态过程仿真');
                if(x*y==0)%如果出现某方士兵数目为0 退出仿真
                    break;
                end
            elseif(x*y<=0)%如果出现某方士兵数目为负数 退出仿真
                break;
            end
         end
         if(x*y<=0)%如果出现某方士兵数目为负数 退出仿真
             break;
         end
      end
       if(x>y)%甲方胜利 乙方失败
          set(handles.xwinflag,'string','胜利,可以乘胜追击');
          set(handles.ywinflag,'string','失败,需要增加兵力，提高军队作战能力');
      elseif(x<y)%甲方失败 乙方胜利
          set(handles.ywinflag,'string','胜利,可以乘胜追击');
          set(handles.xwinflag,'string','失败,需要增加兵力，提高军队作战能力');
      elseif(x==y)%双方战平
          set(handles.ywinflag,'string','双方战为平局');
          set(handles.xwinflag,'string','双方战为平局');
       end
       set(handles.flag,'string','仿真结束');%修改仿真状态 结束仿真
end
end
end
