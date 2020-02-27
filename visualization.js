import * as THREE from './modules/three.module.js';
import TWEEN from './modules/Tween.js';

var targets = [];

var targetGeometry = new THREE.SphereGeometry( 10, 10, 10 );
var targetMaterial = new THREE.MeshBasicMaterial( {color: 0xff0000} );

var entrance = new THREE.Vector3(-50, 0, -175);

var sceneRef;
var cfa111;

var netSystem = 0;




let socket = new WebSocket("ws://localhost:8765");



socket.onmessage = function(event) {
    var dataRaw = event.data;
    var net = 0;
    for(var i = 0; i < dataRaw.length; i++) {
        if(dataRaw[i] == 0) {net += 1;}
        else if(dataRaw[i] == 1 ) {net -= 1;}
    }


    var diff = net - netSystem;
    console.log(net, netSystem);
    if(diff > 0)
        for(var i = 0; i < diff; i++)
            AddTarget(sceneRef);
    else if(diff < 0)
        for(var i = diff; i < 0; i++)
            RemoveTarget(sceneRef);

    netSystem = net;
};





export function GenerateRoom(scene) {

    var material = new THREE.MeshPhongMaterial({
        color: 0x00ff00,
        opacity: 0.3,
        transparent: true,
      });

    cfa111 = new THREE.Mesh( new THREE.BoxGeometry( 200, 75, 350 ), material );
    cfa111.position.set(0,0,0);
    scene.add( cfa111 );

    sceneRef = scene;

}

export function AddTarget(scene) {

    var newTarget = new THREE.Mesh( targetGeometry, targetMaterial );
    newTarget.position.set(entrance);
    scene.add( newTarget );
    targets.push(newTarget);

    var x_scale = cfa111.geometry.parameters.width;
    var y_scale = cfa111.geometry.parameters.height;
    var z_scale = cfa111.geometry.parameters.depth;

    var px = (Math.random()-0.5) * x_scale;
    var py = 0;
    var pz = (Math.random()-0.5) * z_scale;

    var init = entrance.clone();
    var end = { x : px, y: py, z: pz };
    var tween = new TWEEN.Tween(init).to(end, 1500);
    tween.easing(TWEEN.Easing.Quadratic.InOut)
    tween.onUpdate(function(){
        newTarget.position.x = init.x;
        newTarget.position.y = init.y;
        newTarget.position.z = init.z;
    });
    tween.start()

}

export function RemoveTarget(scene) {

    if(targets.length == 0) { return; }
    var target = targets.shift();

    
    var init = target.position;
    var end = entrance.clone();
    var tween = new TWEEN.Tween(init).to(end, 1500);
    tween.easing(TWEEN.Easing.Quadratic.InOut)
    tween.onUpdate(function(){
        target.position.x = init.x;
        target.position.y = init.y;
        target.position.z = init.z;
    });
    tween.start()

    setTimeout(function() { scene.remove(target); }, 1500);
}
