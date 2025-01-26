package com.example.projetSI.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.projetSI.modal.Promo;

@Repository
public interface PromoDao extends JpaRepository<Promo, Integer> {
	Optional<Promo> findPromoById(int id);
}
