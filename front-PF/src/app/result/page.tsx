import * as React from 'react';
import Head from 'next/head';
import Image from 'next/image';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';

const returnedList = [
    "http://localhost:8000/result/graph_decomposition.png",
    "http://localhost:8000/result/outlier_scores.png",
    "http://localhost:8000/result/pca_embeddings.png",
    "http://localhost:8000/result/tsne_embeddings.png"
];

const ImagesPage = () => {
    
    return (
        <Container maxWidth="xl">
            <Head>
                <title>Les résultats</title>
            </Head>
            <Box sx={{ flexGrow: 1, my: 2 }}>
                <Grid container spacing={2} justifyContent="center" alignItems="center">
                    {returnedList.map((imageUrl, index) => (
                        <Grid item xs={12} key={index} sx={{ display: 'flex', justifyContent: 'center' }}>
                            <Image
                                src={imageUrl}
                                alt={`Image ${index + 1}`}
                                width={800}  // Taille ajustée pour une meilleure visibilité
                                height={600}
                                layout="intrinsic"  // 'intrinsic' pour maintenir les proportions sans distorsion
                                unoptimized={true}  // Pour les images externes non optimisées par Next.js
                            />
                        </Grid>
                    ))}
                </Grid>
            </Box>
        </Container>
    );
};

export default ImagesPage;
