import { useEffect, useRef } from 'react';
import lottie from 'lottie-web';

export default function AnimationComponent() {
  // Spécifiez le type de l'élément DOM ici avec useRef<HTMLDivElement>
  const animationContainer = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (animationContainer.current) {
      const anim = lottie.loadAnimation({
        container: animationContainer.current, // Référence au conteneur d'animation
        renderer: 'svg', // Utilise le rendu SVG
        loop: true, // Animation en boucle
        autoplay: true, // Lecture automatique
        path: '/animation/W.json' // Chemin vers votre fichier JSON
      });

      return () => anim.destroy(); // Nettoyez l'animation lors du démontage du composant
    }
  }, []);

  return (
    <div ref={animationContainer} style={{ width: 500, height: 500, marginRight: 30 }} />
  );
}
