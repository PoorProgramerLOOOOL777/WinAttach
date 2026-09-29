<!doctype html>
<html lang="es">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="theme-color" content="#e7e4dc">
	<title>Mano de madera</title>
	<style>
		:root {
			color-scheme: light;
			--scene: #e7e4dc;
			--ink: #252522;
			--button: #faf9f5;
			--button-shadow: #25252220;
		}

		:root[data-theme="dark"] {
			color-scheme: dark;
			--scene: #202522;
			--ink: #f4f0e7;
			--button: #303733;
			--button-shadow: #0000004a;
		}

		* { box-sizing: border-box; }

		html, body { width: 100%; height: 100%; margin: 0; overflow: hidden; }

		body {
			background: var(--scene);
			transition: background-color 260ms ease;
			font-family: Georgia, 'Times New Roman', serif;
		}

		#scene {
			position: fixed;
			inset: 0;
			width: 100%;
			height: 100%;
			display: block;
			cursor: grab;
			touch-action: none;
		}

		#scene:active { cursor: grabbing; }

		#theme-toggle {
			position: fixed;
			z-index: 2;
			top: max(20px, env(safe-area-inset-top));
			right: max(20px, env(safe-area-inset-right));
			width: 48px;
			aspect-ratio: 1;
			display: grid;
			place-items: center;
			border: 1px solid color-mix(in srgb, var(--ink) 18%, transparent);
			border-radius: 50%;
			color: var(--ink);
			background: var(--button);
			box-shadow: 0 4px 18px var(--button-shadow);
			cursor: pointer;
			transition: transform 180ms ease, background-color 260ms ease, color 260ms ease;
		}

		#theme-toggle:hover { transform: rotate(-12deg) scale(1.06); }
		#theme-toggle:focus-visible { outline: 3px solid #bd7446; outline-offset: 4px; }
		#theme-toggle svg { width: 21px; height: 21px; }
		#theme-toggle .sun { display: none; }
		:root[data-theme="dark"] #theme-toggle .moon { display: none; }
		:root[data-theme="dark"] #theme-toggle .sun { display: block; }

		@media (max-width: 600px) {
			#theme-toggle { top: max(14px, env(safe-area-inset-top)); right: max(14px, env(safe-area-inset-right)); width: 44px; }
		}

		@media (prefers-reduced-motion: reduce) {
			*, *::before, *::after { transition-duration: .01ms !important; }
		}
	</style>
</head>
<body>
	<canvas id="scene" aria-label="Mano de madera articulada. Arrastra cualquiera de sus dedos para moverlo."></canvas>
	<button id="theme-toggle" type="button" aria-label="Activar modo oscuro" aria-pressed="false" title="Cambiar modo de luz">
		<svg class="moon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20.2 15.1A8.5 8.5 0 0 1 8.9 3.8 8.5 8.5 0 1 0 20.2 15.1Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
		<svg class="sun" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.8"/><path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
	</button>

	<script type="importmap">
		{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js"}}
	</script>
	<script type="module">
		import * as THREE from 'three';

		const canvas = document.querySelector('#scene');
		const root = document.documentElement;
		const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
		renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
		renderer.shadowMap.enabled = true;
		renderer.shadowMap.type = THREE.PCFSoftShadowMap;
		renderer.outputColorSpace = THREE.SRGBColorSpace;
		renderer.toneMapping = THREE.ACESFilmicToneMapping;
		renderer.toneMappingExposure = 1.18;

		const scene = new THREE.Scene();
		const handModel = new THREE.Group();
		handModel.scale.setScalar(1.12);
		const camera = new THREE.OrthographicCamera(-2.9, 2.9, 3.4, -3.4, 0.1, 50);
		camera.position.set(0, 0, 11);
		camera.lookAt(0, 0, 0);
		scene.add(new THREE.HemisphereLight(0xfff3df, 0x776e61, 2.1));
		const keyLight = new THREE.DirectionalLight(0xffe0b5, 3.2);
		keyLight.position.set(-3.5, 5.5, 7);
		keyLight.castShadow = true;
		keyLight.shadow.mapSize.set(1024, 1024);
		keyLight.shadow.camera.left = -4;
		keyLight.shadow.camera.right = 4;
		keyLight.shadow.camera.top = 5;
		keyLight.shadow.camera.bottom = -5;
		keyLight.shadow.bias = -0.0005;
		scene.add(keyLight);
		const fillLight = new THREE.DirectionalLight(0xd7e1e4, 1.3);
		fillLight.position.set(4, 1, 5);
		scene.add(fillLight);

		const woodCanvas = document.createElement('canvas');
		woodCanvas.width = 512;
		woodCanvas.height = 512;
		const woodContext = woodCanvas.getContext('2d');
		const woodGradient = woodContext.createLinearGradient(0, 0, 512, 512);
		woodGradient.addColorStop(0, '#c9b28c');
		woodGradient.addColorStop(.28, '#e7d5b3');
		woodGradient.addColorStop(.58, '#d4bd96');
		woodGradient.addColorStop(1, '#f0dfbd');
		woodContext.fillStyle = woodGradient;
		woodContext.fillRect(0, 0, 512, 512);
		for (let index = 0; index < 38; index += 1) {
			const x = index * 14 - 2;
			woodContext.beginPath();
			woodContext.moveTo(x, 0);
			woodContext.bezierCurveTo(x + 14 * Math.sin(index), 130, x - 11 * Math.cos(index * .7), 330, x + 5 * Math.sin(index * .4), 512);
			woodContext.strokeStyle = index % 3 === 0 ? 'rgba(111, 83, 53, .15)' : 'rgba(255, 249, 226, .28)';
			woodContext.lineWidth = index % 4 === 0 ? 1.8 : .8;
			woodContext.stroke();
		}
		const woodTexture = new THREE.CanvasTexture(woodCanvas);
		woodTexture.colorSpace = THREE.SRGBColorSpace;
		woodTexture.wrapS = THREE.RepeatWrapping;
		woodTexture.wrapT = THREE.RepeatWrapping;
		woodTexture.anisotropy = renderer.capabilities.getMaxAnisotropy();
		const wood = new THREE.MeshStandardMaterial({ map: woodTexture, roughness: .58, metalness: 0 });
		const darkWood = new THREE.MeshStandardMaterial({ color: 0x987e5e, roughness: .62 });
		const highlightWood = new THREE.MeshStandardMaterial({ color: 0xe8d5b0, roughness: .52 });
		const palmGeometry = new THREE.LatheGeometry([
			[0, -.95], [.3, -.95], [.43, -.88], [.52, -.68], [.58, -.35], [.62, .08], [.61, .35], [.57, .49], [.48, .57], [.27, .61], [0, .62]
		].map(([radius, y]) => new THREE.Vector2(radius, y)), 48);
		palmGeometry.scale(1, 1, .52);
		const palm = new THREE.Mesh(palmGeometry, wood);
		palm.position.y = -.08;
		palm.castShadow = true;
		palm.receiveShadow = true;
		handModel.add(palm);
		const wristGeometry = new THREE.LatheGeometry([
			[0, -2.02], [.26, -2.02], [.32, -1.98], [.35, -1.82], [.37, -1.35], [.39, -.98], [.4, -.84], [.35, -.76], [0, -.74]
		].map(([radius, y]) => new THREE.Vector2(radius, y)), 40);
		wristGeometry.scale(1, 1, .58);
		const wrist = new THREE.Mesh(wristGeometry, wood);
		wrist.castShadow = true;
		wrist.receiveShadow = true;
		handModel.add(wrist);
		const wristSeam = new THREE.Mesh(new THREE.TorusGeometry(.365, .012, 8, 48), darkWood);
		wristSeam.rotation.x = Math.PI / 2;
		wristSeam.position.set(0, -.91, 0);
		handModel.add(wristSeam);

		function makeCapsule(radius, length, material = wood) {
			const mesh = new THREE.Mesh(new THREE.CapsuleGeometry(radius, length, 6, 12), material);
			mesh.castShadow = true;
			mesh.receiveShadow = true;
			return mesh;
		}

		const fingers = [];
		const fingerSpecs = [
			{ name: 'meñique', x: -.43, y: .34, angle: -.13, lengths: [.35, .27, .19], radius: .09 },
			{ name: 'anular', x: -.16, y: .4, angle: -.05, lengths: [.48, .35, .23], radius: .096 },
			{ name: 'medio', x: .12, y: .43, angle: .02, lengths: [.55, .4, .25], radius: .1 },
			{ name: 'índice', x: .39, y: .39, angle: .09, lengths: [.48, .35, .23], radius: .094 }
		];

		for (const spec of fingerSpecs) {
			const base = new THREE.Group();
			base.position.set(spec.x, spec.y, .31);
			base.rotation.z = spec.angle;
			handModel.add(base);
			const first = new THREE.Group();
			base.add(first);
			const joints = [first];
			let parent = first;
			for (let segmentIndex = 0; segmentIndex < spec.lengths.length; segmentIndex += 1) {
				const length = spec.lengths[segmentIndex];
				const segment = makeCapsule(spec.radius * (segmentIndex === 2 ? .86 : 1), length - spec.radius * .8);
				segment.position.y = length / 2;
				segment.userData.finger = spec.name;
				parent.add(segment);
				const joint = new THREE.Mesh(new THREE.SphereGeometry(spec.radius * .92, 16, 12), darkWood);
				joint.position.y = length;
				joint.castShadow = true;
				joint.userData.finger = spec.name;
				parent.add(joint);
				if (segmentIndex < spec.lengths.length - 1) {
					const next = new THREE.Group();
					next.position.y = length;
					parent.add(next);
					joints.push(next);
					parent = next;
				}
			}
			const restAngles = [0.06, 0.28, 0.24];
			joints.forEach((joint, index) => { joint.rotation.z = restAngles[index]; });
			const nail = new THREE.Mesh(new THREE.BoxGeometry(spec.radius * 1.05, spec.lengths[2] * .56, .025), highlightWood);
			nail.position.set(0, spec.lengths[2] * .73, spec.radius * .84);
			nail.userData.finger = spec.name;
			parent.add(nail);
			fingers.push({ name: spec.name, base, joints, restAngles, amount: 0 });
		}

		const thumbBase = new THREE.Group();
		thumbBase.position.set(.5, -.12, .31);
		thumbBase.rotation.z = -.72;
		handModel.add(thumbBase);
		const thumbJointA = new THREE.Group();
		thumbBase.add(thumbJointA);
		const thumbLengths = [.4, .32];
		const thumbJointB = new THREE.Group();
		thumbJointB.position.y = thumbLengths[0];
		thumbJointA.add(thumbJointB);
		const thumbRestAngles = [.08, .18];
		thumbJointA.rotation.z = thumbRestAngles[0];
		thumbJointB.rotation.z = thumbRestAngles[1];
		const thumbSegmentA = makeCapsule(.115, thumbLengths[0] - .09);
		thumbSegmentA.position.y = thumbLengths[0] / 2;
		thumbSegmentA.userData.finger = 'pulgar';
		thumbJointA.add(thumbSegmentA);
		const thumbJoint = new THREE.Mesh(new THREE.SphereGeometry(.102, 16, 12), darkWood);
		thumbJoint.position.y = thumbLengths[0];
		thumbJoint.castShadow = true;
		thumbJoint.userData.finger = 'pulgar';
		thumbJointA.add(thumbJoint);
		const thumbSegmentB = makeCapsule(.103, thumbLengths[1] - .08);
		thumbSegmentB.position.y = thumbLengths[1] / 2;
		thumbSegmentB.userData.finger = 'pulgar';
		thumbJointB.add(thumbSegmentB);
		const thumbNail = new THREE.Mesh(new THREE.BoxGeometry(.105, .16, .025), highlightWood);
		thumbNail.position.set(0, .22, .1);
		thumbNail.userData.finger = 'pulgar';
		thumbJointB.add(thumbNail);
		fingers.push({ name: 'pulgar', base: thumbBase, joints: [thumbJointA, thumbJointB], restAngles: thumbRestAngles, amount: 0 });
		scene.add(handModel);

		const raycaster = new THREE.Raycaster();
		const pointer = new THREE.Vector2();
		let activeFinger = null;
		let lastPointerY = 0;

		function findFingerObject(object) {
			let current = object;
			while (current) {
				if (current.userData.finger) return current.userData.finger;
				current = current.parent;
			}
			return null;
		}

		canvas.addEventListener('pointerdown', event => {
			const bounds = canvas.getBoundingClientRect();
			pointer.x = ((event.clientX - bounds.left) / bounds.width) * 2 - 1;
			pointer.y = -((event.clientY - bounds.top) / bounds.height) * 2 + 1;
			raycaster.setFromCamera(pointer, camera);
			const hit = raycaster.intersectObjects(scene.children, true).find(intersection => findFingerObject(intersection.object));
			if (!hit) return;
			const name = findFingerObject(hit.object);
			activeFinger = fingers.find(finger => finger.name === name);
			lastPointerY = event.clientY;
			canvas.setPointerCapture(event.pointerId);
			event.preventDefault();
		});

		canvas.addEventListener('pointermove', event => {
			if (!activeFinger) return;
			const delta = event.clientY - lastPointerY;
			lastPointerY = event.clientY;
			activeFinger.amount = THREE.MathUtils.clamp(activeFinger.amount + delta * .009, 0, 1);
			const rotation = activeFinger.amount * .8;
			activeFinger.joints.forEach((joint, index) => {
				joint.rotation.z = activeFinger.restAngles[index] + rotation * [0.45, 0.72, 0.55][index];
			});
		});

		function endDrag() { activeFinger = null; }
		canvas.addEventListener('pointerup', endDrag);
		canvas.addEventListener('pointercancel', endDrag);

		const toggle = document.querySelector('#theme-toggle');
		toggle.addEventListener('click', () => {
			const dark = root.dataset.theme !== 'dark';
			root.dataset.theme = dark ? 'dark' : 'light';
			toggle.setAttribute('aria-pressed', String(dark));
			toggle.setAttribute('aria-label', dark ? 'Activar modo claro' : 'Activar modo oscuro');
			scene.background = new THREE.Color(dark ? '#202522' : '#e7e4dc');
			keyLight.intensity = dark ? 2.4 : 3.2;
			fillLight.intensity = dark ? 1.8 : 1.3;
		});
		scene.background = new THREE.Color('#e7e4dc');

		function resize() {
			const width = window.innerWidth;
			const height = window.innerHeight;
			const aspect = width / height;
			const viewHeight = 4.7;
			camera.left = -viewHeight * aspect / 2;
			camera.right = viewHeight * aspect / 2;
			camera.top = viewHeight / 2;
			camera.bottom = -viewHeight / 2;
			camera.updateProjectionMatrix();
			renderer.setSize(width, height, false);
		}
		window.addEventListener('resize', resize);
		resize();

		function animate() {
			requestAnimationFrame(animate);
			renderer.render(scene, camera);
		}
		animate();
	</script>
</body>
</html>