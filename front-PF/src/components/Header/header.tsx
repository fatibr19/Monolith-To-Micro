'use client'
import { useState } from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Menu, MenuItem } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import Link from 'next/link';
import Image from "next/image";
import { usePathname } from 'next/navigation';

interface NavItem {
  label: string;
  href: string;
}

interface HeaderProps {
  logo?: string;
  navItems?: NavItem[];
}

const defaultNavItems: NavItem[] = [
  { label: 'Accueil', href: '/' },
  { label: 'À propos', href: '/about' },
];

export default function Header({ 
  logo = '/ensias.png',
  navItems = defaultNavItems
}: HeaderProps) {
  const pathname = usePathname();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  // Filtrer les éléments du menu en fonction du pathname
  const filteredNavItems = pathname === '/about'
    ? [{ label: 'Accueil', href: '/' }]
    : [{ label: 'À propos', href: '/about' }];

  const handleMenuOpen = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar position="static" sx={{ 
      backgroundColor: '#FFFFFF', 
      color: 'black', 
      boxShadow: '0px 0px 27px rgba(0, 0, 0, 0.15)', 
      padding: "20px", 
      fontFamily: "'JetBrains Mono', monospace"  // Applying JetBrains Mono to all AppBar
    }}>

      <Toolbar>
        {/* Logo */}
        <Link href="/" passHref >
          <Image 
            src={logo}
            alt="Logo du site"
            width={220}
            height={80}
            priority
            style={{ cursor: 'pointer', marginRight: 16 }}
            
            
          />
        </Link>

        {/* Titre */}
        <Typography variant="h6" sx={{ml:"20%",flexGrow: 3 }} style={{ fontFamily: 'JetBrains Mono, monospace' }} >
          PF : Décomposition des Monoliths en Microservices
        </Typography>

        {/* Menu pour écrans larges */}
        <div className="nav-desktop">
          {filteredNavItems.map((item, index) => (
            <Button 
              key={index} 
              color="inherit"
              component={Link} 
              href={item.href}
              sx={{ fontWeight: pathname === item.href ? 'bold' : 'normal' }}
              style={{ fontFamily: 'JetBrains Mono, monospace' }}
            >
              {item.label}
            </Button>
          ))}
        </div>

        {/* Menu burger pour mobile */}
        <IconButton 
          edge="end"
          color="inherit"
          aria-label="menu"
          onClick={handleMenuOpen}
          sx={{ display: { xs: 'block', sm: 'none' } }}
        >
          <MenuIcon />
        </IconButton>

        {/* Menu déroulant mobile */}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
        >
          {filteredNavItems.map((item, index) => (
            <MenuItem 
              key={index} 
              onClick={handleMenuClose} 
              component={Link} 
              href={item.href}
            >
              {item.label}
            </MenuItem>
          ))}
        </Menu>
      </Toolbar>
    </AppBar>
  );
}
