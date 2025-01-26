import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Button, Card, Typography } from "@mui/material";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";
import axios from 'axios';

function StyledDropzone() {
  const [fileInfo, setFileInfo] = useState<{ file: File; size: string } | null>(null);

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

  const handleSubmit = async () => { // Ajout de async ici
    if (fileInfo) {
      const formData = new FormData();
      formData.append("file", fileInfo.file); // Correction ici, passer fileInfo.file

      try {
        const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        alert('File uploaded successfully');
        console.log(response.data);
      } catch (error) {
        alert('Error uploading file');
        console.error('Error uploading file:', error);
      }
    } else {
      alert("Please upload a .zip file");
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
        {...getRootProps()}
        sx={{
          padding: "1px",
          border: "2px dashed #1f216f",
        }}
      >
        <Card
          sx={{
            padding: 2,
            textAlign: "center",
            background: fileInfo ? "#FFFFFF" : "#1f216f",
            color: fileInfo ? "#000000" : "#FFF",
          }}
        >
          <input {...getInputProps()} />
          {fileInfo ? (
            <>
              <InsertDriveFileIcon sx={{ fontSize: 60 }} />
              <Typography variant="body1" sx={{ fontFamily: "'JetBrains Mono', monospace" }}>
                {fileInfo.file.name} - {fileInfo.size}
              </Typography>
            </>
          ) : (
            <Typography variant="body2" sx={{ fontFamily: "'JetBrains Mono', monospace" }}>
              {isDragActive ? "Déposez votre fichier ici..." : "Glissez et déposez votre fichier .zip ici ou cliquez pour sélectionner un fichier"}
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
