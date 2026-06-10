import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';
import useBaseUrl from '@docusaurus/useBaseUrl';

type FeatureItem = {
  title: string;
  image: string;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Commvault',
    image: '/img/cv.jpg',
    description: (
      <>
        Data protection and recovery solution used to back up and restore CBA and Bankwest data.
      </>
    ),
  },
  {
    title: 'Databunker',
    image: '/img/db.png',
    description: (
      <>
        Data Bunker is a data protection zone for CBA and Bankwest critical data.
      </>
    ),
  },
  {
    title: 'Isolated Recovery Environments',
    image: '/img/ire.png',
    description: (
      <>
        CBA Isolated Recovery Environments (IRE) provide a secure, air-gapped environment to recover critical data.
      </>
    ),
  },
  {
    title: 'Bankwest',
    image: '/img/bw.png',
    description: (
      <>
        Bankwest data protection and recovery documentation.
      </>
    ),
  },
];

function Feature({ image, title, description }: FeatureItem) {
  return (
    <div className={clsx('col col--3')}>
      <div className="text--center">
        <img alt={title} className={styles.featureImg} role="img" src={useBaseUrl(image)} />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}