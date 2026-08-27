import React, { Suspense, useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Canvas, useFrame } from '@react-three/fiber';
import { Environment, OrbitControls, useGLTF } from '@react-three/drei';
import * as THREE from 'three';
import { generateHanys3D } from './generate3d.js';
import './styles.css';

const REFERENCE_IMAGE = 'https://raw.githubusercontent.com/bajerskim11-eng/beboki-gra/hanys-demo/hanys-demo%2Fhanys-demo%3Aassets%3Ahanys-reference.png';

function HanysModel({ action, modelUrl }) {
  const group = useRef();
  const { scene } = useGLTF(modelUrl);
  useEffect(() => { scene.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); }, [scene]);
  useFrame((state, delta) => {
    if (!group.current) return;
    const t = state.clock.elapsedTime;
    group.current.position.y = Math.sin(t * 1.7) * 0.025;
    group.current.rotation.y = Math.sin(t * 0.35) * 0.035;
    if (action === 'jump') group.current.position.y += Math.max(0, Math.sin(t * 7)) * 0.7;
    if (action === 'happy') group.current.rotation.z = Math.sin(t * 5) * 0.06;
    else group.current.rotation.z = THREE.MathUtils.damp(group.current.rotation.z, 0, 8, delta);
  });
  return <primitive ref={group} object={scene} scale={2.3} position={[0, -1.4, 0]} />;
}

function Scene({ action, modelUrl, setReady }) {
  return <Canvas shadows camera={{ position: [0, 0.3, 4.2], fov: 38 }} onCreated={() => setReady(true)}>
    <ambientLight intensity={1.7} /><directionalLight castShadow position={[3, 5, 4]} intensity={3} shadow-mapSize={[1024, 1024]} />
    <Environment preset="city" /><Suspense fallback={null}><HanysModel action={action} modelUrl={modelUrl} /></Suspense>
    <OrbitControls enablePan={false} minDistance={2.8} maxDistance={6} minPolarAngle={1.0} maxPolarAngle={2.15} />
  </Canvas>;
}

function App() {
  const [action, setAction] = useState('idle');
  const [modelUrl, setModelUrl] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [message, setMessage] = useState('Cześć! Jestem Hanyś.');
  const [ready, setReady] = useState(false);

  const react = next => { setAction(next); setMessage(next === 'jump' ? 'Hop!' : 'No to lecimy! 😄'); window.setTimeout(() => { setAction('idle'); setMessage('Cześć! Jestem Hanyś.'); }, next === 'jump' ? 900 : 1200); };

  async function create3D() {
    try {
      setGenerating(true); setMessage('NVIDIA tworzy mojego Hanysa… 🧌');
      const response = await fetch(REFERENCE_IMAGE); const blob = await response.blob();
      const file = new File([blob], 'hanys-reference.png', { type: blob.type || 'image/png' });
      const bytes = await generateHanys3D(file);
      const url = URL.createObjectURL(new Blob([bytes], { type: 'model/gltf-binary' }));
      setModelUrl(url); setReady(false); setMessage('Gotowe! Jestem w 3D. 🔥');
    } catch (e) { console.error(e); setMessage(`Błąd: ${e.message}`); }
    finally { setGenerating(false); }
  }

  return <main className="app">
    <header className="topbar"><strong>HANYŚ</strong><span>Twój Bebok</span><div className="stats">❤️ 100&nbsp;&nbsp; ⭐ 0</div></header>
    <section className="stage">
      {modelUrl ? <Scene action={action} modelUrl={modelUrl} setReady={setReady} /> : <div className="reference"><img src={REFERENCE_IMAGE} alt="Hanyś – model referencyjny" /><div>{generating ? 'Generowanie modelu 3D…' : 'Najpierw stwórz mojego Hanysa 3D'}</div></div>}
      <div className="speech">{message}</div>
    </section>
    <section className="actions">
      {!modelUrl && <button onClick={create3D} disabled={generating}>🧌 {generating ? 'Tworzę 3D…' : 'Stwórz Hanysa 3D'}</button>}
      {modelUrl && <><button onClick={() => react('happy')}>👋 Przywitaj się</button><button onClick={() => react('jump')}>🦘 Skok</button><button onClick={() => react('happy')}>❤️ Pogłaszcz</button><button onClick={() => react('talk')}>🎤 Porozmawiaj</button></>}
    </section>
    <p className="status">{modelUrl ? (ready ? 'Hanyś 3D jest załadowany.' : 'Ładowanie modelu 3D…') : 'Pipeline: zdjęcie → NVIDIA TRELLIS → GLB → Three.js'}</p>
  </main>;
}
createRoot(document.getElementById('root')).render(<App />);
