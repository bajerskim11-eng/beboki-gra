import React, { Suspense, useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Canvas, useFrame } from '@react-three/fiber';
import { Environment, OrbitControls, useGLTF } from '@react-three/drei';
import * as THREE from 'three';
import './styles.css';

const REFERENCE_IMAGE = 'https://raw.githubusercontent.com/bajerskim11-eng/beboki-gra/hanys-demo/hanys-demo%2Fhanys-demo%3Aassets%3Ahanys-reference.png';

function HanysModel({ action }) {
  const group = useRef();
  const { scene } = useGLTF('/models/hanys.glb');

  useEffect(() => {
    scene.traverse((o) => {
      if (o.isMesh) {
        o.castShadow = true;
        o.receiveShadow = true;
      }
    });
  }, [scene]);

  useFrame((state, delta) => {
    if (!group.current) return;
    const t = state.clock.elapsedTime;
    group.current.position.y = Math.sin(t * 1.7) * 0.025;
    group.current.rotation.y = Math.sin(t * 0.35) * 0.035;
    if (action === 'jump') {
      group.current.position.y += Math.max(0, Math.sin(t * 7)) * 0.7;
    }
    if (action === 'happy') group.current.rotation.z = Math.sin(t * 5) * 0.06;
    else group.current.rotation.z = THREE.MathUtils.damp(group.current.rotation.z, 0, 8, delta);
  });

  return <primitive ref={group} object={scene} scale={2.3} position={[0, -1.4, 0]} />;
}

function Scene({ action, setReady }) {
  return (
    <Canvas shadows camera={{ position: [0, 0.3, 4.2], fov: 38 }} onCreated={() => setReady(true)}>
      <ambientLight intensity={1.7} />
      <directionalLight castShadow position={[3, 5, 4]} intensity={3} shadow-mapSize={[1024, 1024]} />
      <Environment preset="city" />
      <Suspense fallback={null}>
        <HanysModel action={action} />
      </Suspense>
      <OrbitControls enablePan={false} minDistance={2.8} maxDistance={6} minPolarAngle={1.0} maxPolarAngle={2.15} />
    </Canvas>
  );
}

function App() {
  const [action, setAction] = useState('idle');
  const [modelError, setModelError] = useState(false);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    fetch('/models/hanys.glb', { method: 'HEAD' }).catch(() => setModelError(true));
  }, []);

  const react = (next) => {
    setAction(next);
    window.setTimeout(() => setAction('idle'), next === 'jump' ? 900 : 1200);
  };

  return (
    <main className="app">
      <header className="topbar"><strong>HANYŚ</strong><span>Twój Bebok</span><div className="stats">❤️ 100&nbsp;&nbsp; ⭐ 0</div></header>
      <section className="stage">
        {!modelError ? <Scene action={action} setReady={setReady} /> : <div className="reference"><img src={REFERENCE_IMAGE} alt="Hanyś – model referencyjny" /><div>Model 3D będzie tutaj</div></div>}
        <div className="speech">{action === 'jump' ? 'Hop!' : action === 'happy' ? 'No to lecimy! 😄' : 'Cześć! Jestem Hanyś.'}</div>
      </section>
      <section className="actions">
        <button onClick={() => react('happy')}>👋 Przywitaj się</button>
        <button onClick={() => react('jump')}>🦘 Skok</button>
        <button onClick={() => react('happy')}>❤️ Pogłaszcz</button>
        <button onClick={() => react('talk')}>🎤 Porozmawiaj</button>
      </section>
      <p className="status">{modelError ? 'Czekamy na hanys.glb — ekran referencyjny działa.' : ready ? 'Hanyś 3D jest załadowany.' : 'Ładowanie Hanysa…'}</p>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
