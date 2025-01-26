"use client"
import React, { useState, ChangeEvent, FormEvent, useEffect } from 'react';
import { Card, CardContent, TextField, Button, Typography, Box } from '@mui/material';
import { useSearchParams } from 'next/navigation';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import LoadingComponent from '../loading';

const MicroserviceForm: React.FC = () => {
    const [numMicroservices, setNumMicroservices] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [imageUrl, setImageUrl] = useState<string | null>(null);
    const [zipUrl, setzipUrl] = useState<string | null>(null);
    const searchParams = useSearchParams();
    const router = useRouter()
    
    console.log(numMicroservices)
    console.log(zipUrl)

    useEffect(() => {
        // Log all search parameters for debugging
        console.log('All search params:', Object.fromEntries(searchParams));
        
        // Retrieve image URL from search parameters
        const imageParam = searchParams.get('image');
        console.log('Raw image param:', imageParam);
        const zipPath = searchParams.get('zip_path');
        console.log('zip path param', zipPath)

        if (imageParam) {
            const fullImageUrl = `http://127.0.0.1:8000${imageParam}`;
            console.log('Full image URL:', fullImageUrl);
            setImageUrl(fullImageUrl);
        }

        if(zipPath){
            setzipUrl(zipPath)
        }
    }, [searchParams]);

    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        setNumMicroservices(event.target.value);
    };

    const handleSubmit = async (event: FormEvent) => {
        event.preventDefault();
        try {
            setIsLoading(true);
            const response = await axios.post('http://127.0.0.1:8000/set_microservices/', {
                number_of_microservices: numMicroservices,
                zip_file: zipUrl || '', // Provide a default empty string if zipUrl is null
            });
            alert(`Réponse du serveur: ${response.data.message}`);
            router.push(`/result`)
            setIsLoading(false);
        } catch (error) {
            console.error('Erreur lors de l\'envoi des données:', error);
            alert('Erreur lors de l\'envoi des données. Vérifiez la console pour plus de détails.');
            setIsLoading(false);
        }
    };

    return (
        <Card sx={{ maxWidth: 800, mx: 'auto', mt: 5 }}>
            <CardContent>
                <Typography variant="h5" component="div" gutterBottom sx={{ fontFamily: "'JetBrains Mono', monospace" }}>
                    Configuration des Microservices
                </Typography>
                {imageUrl ? (
                    <Box
                        component="img"
                        sx={{
                            
                            maxHeight: { xs: 233, md: 500 },
                            maxWidth: { xs: 350, md: 500 },
                            display: 'block',
                            fontFamily: "'JetBrains Mono', monospace",
                            mx: 'auto'
                        }}
                        src={imageUrl}
                        alt="Image de configuration"
                    />
                ) : (
                    <Box
                        component="img"
                        sx={{
                            height: 500,
                            width: 500,
                            maxHeight: { xs: 233, md: 500 },
                            maxWidth: { xs: 350, md: 500 },
                            display: 'block',
                            fontFamily: "'JetBrains Mono', monospace",
                            mx: 'auto'
                        }}
                        src="https://via.placeholder.com/500"
                        alt="Image de configuration"
                    />
                )}
                <form onSubmit={handleSubmit}>
                    <TextField
                        fullWidth
                        type="number"
                        label="Nombre de microservices"
                        variant="outlined"
                        value={numMicroservices}
                        onChange={handleChange}
                        margin="normal"
                        sx={{ fontFamily: "'JetBrains Mono', monospace" }}
                    />
                    <Button type="submit" variant="contained" sx={{ mt: 2, fontFamily: "'JetBrains Mono', monospace" }}>
                        Confirmer
                    </Button>

                </form>
                {isLoading && (
                        <LoadingComponent/>
                      )}
            </CardContent>
        </Card>
    );
}

export default MicroserviceForm;