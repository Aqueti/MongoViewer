/*
gyro plugin for KRPanoJS and iOS4.2+
by Aldo Hoeben / fieldOfView.com
contributions by 
	Sjeiti / ronvalstar.nl
	Klaus / krpano.com
	
http://fieldofview.github.com/krpano_fovplugins/gyro/plugin.html
This software can be used free of charge and the source code is available under a Creative Commons Attribution license:
	http://creativecommons.org/licenses/by/3.0/	
*/
var krpanoplugin=function(){function p(){C=!1;q=null;void 0===r?g=!0:r&&!g?(window.addEventListener("deviceorientation",H,!0),b.control.layer.addEventListener("touchstart",I,!0),b.control.layer.addEventListener("touchend",y,!0),b.control.layer.addEventListener("touchcancel",y,!0),g=!0,z=-(s?top.orientation:window.orientation),t=m=f=0,k=b.view.camroll):g=!1}function A(){r&&g&&(window.removeEventListener("deviceorientation",H,!0),b.control.layer.removeEventListener("touchstart",I),b.control.layer.removeEventListener("touchend", y),b.control.layer.removeEventListener("touchcancel",y));B&&b.call("tween(view.camroll,0)");g=!1}function J(){g?A():p()}function D(){r=!0;window.removeEventListener("deviceorientation",D);g&&(g=!1,p());null!=d.onavailable&&b.call(d.onavailable,d)}function I(){E=!0}function y(){E=!1}function H(n){if(!E&&g){var d=s?top.orientation:window.orientation,l,a=n.alpha*u,h=n.beta*u,c=n.gamma*u,e;e=Math.cos(a);var a=Math.sin(a),i=Math.cos(h),h=Math.sin(h),j=Math.cos(c),c=Math.sin(c),a=[a*c-e*h*j,-e*i,e*h*c+ a*j,i*j,-h,-i*c,a*h*j+e*c,a*i,-a*h*c+e*j];0.9999<a[3]?(e=Math.atan2(a[2],a[8]),a=Math.PI/2,c=0):-0.9999>a[3]?(e=Math.atan2(a[2],a[8]),a=-Math.PI/2,c=0):(e=Math.atan2(-a[6],a[0]),c=Math.atan2(-a[5],a[4]),a=Math.asin(a[3]));l={yaw:e,pitch:a,roll:c};e=v(l.yaw/u);var c=l.pitch/u,a=e,i=b.view.hlookat,h=b.view.vlookat,j=b.view.camroll,r=i-m,p=h-t;if(C){B&&(k=v(180+Number(d)-l.roll/u));if(70<Math.abs(c)){a=n.alpha;switch(d){case 0:0<c&&(a+=180);break;case 90:a+=90;break;case -90:a+=-90;break;case 180:0> c&&(a+=180)}a=v(a);180<Math.abs(a-e)&&(a+=a<e?360:-360);n=Math.min(1,(Math.abs(c)-70)/10);e=e*(1-n)+a*n;k*=1-n}z+=r;f+=p;90<Math.abs(c+f)&&(f=0<c+f?90-c:-90-c);m=v(-e-180+z);t=Math.max(Math.min(c+f,90),-90);180<Math.abs(m-i)&&(i+=m>i?360:-360);m=(1-o)*m+o*i;t=(1-o)*t+o*h;180<Math.abs(k-j)&&(j+=k>j?360:-360);k=(1-o)*k+o*j;b.view.hlookat=v(m);b.view.vlookat=t;b.view.camroll=v(k);0!=f&&0<x&&(0==p?1==x?w=f=0:(w=1-(1-w)*b.control.touchfriction,f*=1-Math.pow(x,2)*w,0.1>Math.abs(f)&&(w=f=0)):w=0)}else if(null== q)q=l;else if(l.yaw!=q.yaw||l.pitch!=q.pitch||l.roll!=q.roll)q=null,C=!0,F&&(f=-c)}}function v(b){b%=360;return 180>=b?b:b-360}function G(b){return 0<="yesontrue1".indexOf((""+b).toLowerCase())}var b=null,d=null,s=!1,r,g=!1,x=0,F=!1,B=!1,o=0.5,E=!1,C=!1,q=null,z=0,f=0,m=0,t=0,k=0,w=0,u=Math.PI/180;this.registerplugin=function(f,k,l){b=f;d=l;if("1.0.8.14">b.version||"2011-03-30">b.build)b.trace(3,"gyro plugin - too old krpano version (min. 1.0.8.14)");else{s=b._have_top_access;if(void 0===s){s=!1; try{top&&top.document&&(s=!0)}catch(a){}}window.DeviceOrientationEvent&&window.addEventListener("deviceorientation",D);d.registerattribute("available",!1,function(){},function(){return r});d.registerattribute("enabled",!0,function(a){G(a)?p():A()},function(){return g});d.registerattribute("velastic",0,function(a){x=Math.max(Math.min(Number(a),1),0)},function(){return x});d.registerattribute("vrelative",!1,function(a){F=G(a)},function(){return F});d.registerattribute("camroll",!1,function(a){B=G(a)}, function(){return B});d.registerattribute("friction",0.5,function(a){o=Math.max(Math.min(Number(a),1),0)},function(){return o});d.registerattribute("onavailable",null);d.enable=p;d.disable=A;d.toggle=J}};this.unloadplugin=function(){window.removeEventListener("deviceorientation",D);A();b=d=null}};