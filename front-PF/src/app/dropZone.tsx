import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Button, Card, Typography } from "@mui/material";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";

function StyledDropzone() {
  const [fileInfo, setFileInfo] = useState<{ file: File; size: string } | null>(
    null
  );

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file && (file.type === "application/x-zip-compressed" || file.type === "application/zip")) {
      setFileInfo({
        file,
        size: (file.size / 1024 / 1024).toFixed(2) + " MB", // Conversion de la taille en MB
      });
    } else {
      alert("Veuillez déposer un fichier .zip valide!");
      setFileInfo(null); // Réinitialiser les infos du fichier si incorrect
    }
  }, []);

  const handleSubmit = () => {
    if (fileInfo) {
      console.log("Envoi du fichier:", fileInfo.file);
      alert("Fichier envoyé avec succès !");
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/zip": [".zip"] },
    maxFiles: 1
  });

  return (
    <>
      <Card
        sx={{
          padding: "1px",
          border: "2px dashed #1f216f",
        }}
      >
        <Card
          {...getRootProps()}
          sx={{
            padding: 2,
            textAlign: "center",
            background: fileInfo ? "#FFFFFF" : "#1f216f", // Changement de fond après le téléchargement
            color: fileInfo ? "#000000" : "#FFF", // Changement de couleur de texte
          }}
        >
          <input {...getInputProps()} />
          {fileInfo ? (
            <>
              <InsertDriveFileIcon sx={{ fontSize: 60 }} />
              <Typography
                variant="body1"
                sx={{ fontFamily: "'JetBrains Mono', monospace" }}
              >
                {fileInfo.file.name} - {fileInfo.size}
              </Typography>
              
            </>
          ) : (
            <Typography
              variant="body2"
              sx={{ fontFamily: "'JetBrains Mono', monospace" }}
            >
              {isDragActive
                ? "Déposez votre fichier ici..."
                : "Glissez et déposez votre fichier .zip ici ou cliquez pour sélectionner un fichier"}
            </Typography>
          )}
        </Card>
      </Card>
      {fileInfo && (
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          sx={{
            fontFamily: "'JetBrains Mono', monospace",
            mt: 2,
            ml: "100px"
          }}
        >
          Envoyer le fichier
        </Button>
      )}
    </>
  );
}

export default StyledDropzone;
