package com.example.statistiques;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.YearMonth;
import java.util.HashMap;
import java.util.Map;

@Service
public class CommandeConsumer {

    // Nombre de commandes par produit
    private final Map<String, Integer> commandesParProduit = new HashMap<>();

    // Chiffre d'affaires par mois
    private final Map<YearMonth, Double> chiffreAffairesParMois = new HashMap<>();

    @KafkaListener(
            topics = "commandes-creees",
            groupId = "statistiques-group"
    )
    public void recevoirCommande(Commande commande) {

        // 1. Compter les commandes par produit
        String produit = commande.getProduit();

        commandesParProduit.put(
                produit,
                commandesParProduit.getOrDefault(produit, 0) + 1
        );

        // 2. Calculer le chiffre d'affaires du mois
        if (commande.getDate() != null) {

            LocalDateTime date =
                    LocalDateTime.parse(commande.getDate());

            YearMonth mois = YearMonth.from(date);

            chiffreAffairesParMois.put(
                    mois,
                    chiffreAffairesParMois.getOrDefault(mois, 0.0)
                            + commande.getMontant()
            );
        }

        // 3. Afficher les statistiques
        System.out.println();
        System.out.println("================================");
        System.out.println("STATISTIQUES");
        System.out.println("================================");

        System.out.println(
                "Nouvelle commande : "
                        + commande.getCommande_id()
        );

        System.out.println(
                "Produit : "
                        + commande.getProduit()
        );

        System.out.println(
                "Montant : "
                        + commande.getMontant()
                        + " €"
        );

        System.out.println();
        System.out.println("Commandes par produit :");

        for (Map.Entry<String, Integer> entry
                : commandesParProduit.entrySet()) {

            System.out.println(
                    entry.getKey()
                            + " : "
                            + entry.getValue()
            );
        }

        System.out.println();
        System.out.println("Chiffre d'affaires par mois :");

        for (Map.Entry<YearMonth, Double> entry
                : chiffreAffairesParMois.entrySet()) {

            System.out.println(
                    entry.getKey()
                            + " : "
                            + entry.getValue()
                            + " €"
            );
        }

        System.out.println("================================");
    }
}

