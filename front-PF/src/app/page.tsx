"use client"
import { Card, CardContent,  Typography, useTheme } from '@mui/material';

import { useState, ChangeEvent } from 'react';
import AnimationComponent from './animation';
import StyledDropzone from './dropZone';

export default function Home() {
  const theme = useTheme();
  const [file, setFile] = useState<File | null>(null);
 

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      setFile(files[0]);
    }
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log('Fichier à traiter:', file?.name);
  };

  return (
    <main style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '20px', boxShadow:"none" }}>
      <Card 
      
        elevation={0}
        sx={{
          maxWidth: 450,
          width: '100%',
          mr: "200px"
        }}>
        <CardContent>
          <Typography gutterBottom variant="h5" sx={{fontFamily: "'JetBrains Mono', monospace"}}>
            Uploadez Votre Monolithe
          </Typography>
          
          <StyledDropzone/>
          
          
        </CardContent>
        
      </Card>
      <AnimationComponent />
    </main>
  );
}
