"use client"
import { useEffect, useRef } from 'react';
import lottie from 'lottie-web';

export default function LoadingComponent() {
  // Spécifiez le type de l'élément DOM ici avec useRef<HTMLDivElement>
  const animationContainer = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (animationContainer.current) {
      const anim = lottie.loadAnimation({
        container: animationContainer.current, // Référence au conteneur d'animation
        renderer: 'svg', // Utilise le rendu SVG
        loop: true, // Animation en boucle
        autoplay: true, // Lecture automatique
        path: '/animation/A.json' // Chemin vers votre fichier JSON
      });

      return () => anim.destroy(); // Nettoyez l'animation lors du démontage du composant
    }
  }, []);

  return (
    <div ref={animationContainer} style={{ width: 100, height: 100, marginLeft: 160 }} />
  );
}
