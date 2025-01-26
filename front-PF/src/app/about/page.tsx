import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

function ProjectDescription() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <Card sx={{
          maxWidth: '80%', // Use 80% of the parent's width
          width: '100%', // Ensure the card can stretch up to 80% of the parent
          margin: '100px', // Center the card horizontally
          padding: 2,
          border: "20px",
          borderRadius: '16px',
          backgroundColor: '#f5f5f5',
          fontFamily: "'JetBrains Mono', monospace", // Applies JetBrains Mono to all text
        }}>
        <CardContent>
          <Typography variant="h5" gutterBottom component="div" sx={{ fontFamily: "'JetBrains Mono', monospace" }}>
            Projet Fédérateur
          </Typography>
          <Typography variant="body1" sx={{ fontFamily: "'JetBrains Mono', monospace" }}>
            Réalisé par <strong>Nour AMELLOUK</strong>, <strong>Fatima Ezzahra BRAIKAT</strong>, et <strong>Hiba MEKKAOUI</strong> sous l'encadrement de Monsieur <strong>Karim BAINA</strong>, notre cher professeur, et en collaboration avec :
          </Typography><br />
          <ul style={{paddingLeft:'3rem'}} >
            <li><strong>Sbai Hanae</strong>, professeur à FST Mohammedia,</li>
            <li><strong>AIT MANSOUR Nassima</strong>, doctorante-chercheuse en cotutelle (FST Mohammedia, ENSIAS Rabat) et enseignante-chercheuse à l'École Marocaine des Sciences de l'Ingénieur (EMSI),</li>
            <li><strong>Manal Gasmi</strong>, étudiante en première année de doctorat à l’ENSIAS et</li>
            <li><strong>Aicham MOHAMED</strong>, doctorant 1ère année à l'ENSIAS.</li>
          </ul><br />
          <Typography variant="body1" paragraph sx={{ fontFamily: "'JetBrains Mono', monospace" }}>
            Ce projet vise à permettre la décomposition des monolithes développés en Spring Boot en plusieurs microservices. Cette initiative permet aux utilisateurs de choisir le nombre de microservices désirés,
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
