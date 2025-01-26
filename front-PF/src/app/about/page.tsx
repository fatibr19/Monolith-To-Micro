import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

function ProjectDescription() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
      <Card sx={{
          maxWidth: '80%', // Utilise 80% de la largeur du parent
          width: '100%', // Assure que la carte peut s'étendre jusqu'à 80% du parent
          margin: '100px', // Centre la carte horizontalement
          padding: 2,
          border:"20px",
          borderRadius: '16px',
          backgroundColor: '#f5f5f5',
          fontFamily: "'JetBrains Mono', monospace", // Applique JetBrains Mono à tous les textes
        }}>
        <CardContent>
          <Typography variant="h5" gutterBottom component="div" sx={{ fontFamily: "'JetBrains Mono', monospace" }}>
            Projet Fédérateur
          </Typography>
          <Typography variant="body1" paragraph sx={{ fontFamily: "'JetBrains Mono', monospace" }}>
            Réalisé par Nour AMELLOUK, Braikat Fatima Ezzahra, et Mekkaoui Hiba sous l'encadrement de Monsieur Karim BAINA,
            notre professeur, et avec la collaboration de ses doctorants, ce projet vise à permettre la décomposition des monolithes développés en Spring Boot
            en plusieurs microservices. Cette initiative permet aux utilisateurs de choisir le nombre de microservices désirés,
            facilitant ainsi la migration d'architectures complexes.
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ fontFamily: "'JetBrains Mono', monospace" }}>
            L'objectif est de simplifier la transition vers des architectures basées sur les microservices, offrant une meilleure
            scalabilité, une maintenance plus aisée et une optimisation des performances.
          </Typography>
        </CardContent>
      </Card>
    </div>
  );
}

export default ProjectDescription;
