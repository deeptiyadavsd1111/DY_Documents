import React from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
// import HomepageFeatures from '@site/src/components/HomepageFeatures';
import HomepageFeatures from '../components/HomepageFeatures';
import * as LDClient from 'launchdarkly-js-client-sdk';
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';
import { isIE, isChrome, isSafari, isIOS, isFirefox, isOpera, isEdge, isLegacyEdge } from 'react-device-detect';

// import Heading from '@theme/Heading';
import styles from './index.module.css';

function getBrowserType() {
  if (ExecutionEnvironment.canUseDOM) {
    if (isIE) return "internet_explorer";
    else if (isChrome) return "chrome";
    else if (isSafari) return "safari";
    else if (isIOS) return "ios";
    else if (isFirefox) return "firefox";
    else if (isOpera) return "opera";
    else if (isEdge) return "edge";
    else if (isLegacyEdge) return "legacy-edge";
    else return "unknown";
  }
  return "unknown";
}

function HomepageHeader() {
  const [, setBannerType] = React.useState("heroBanner");
  const context = {
    kind: 'browser',
    key: getBrowserType(),
  };
  // const accessTime = new Date().toISOString();
  if (ExecutionEnvironment.canUseDOM) {
    const localClient = LDClient.initialize('662613e2d4d0be0f578f9faf', context);
    localClient.waitUntilReady().then(() => {
      const variation = localClient.variation('banner', 'heroBanner');
      setBannerType(variation);
      localClient.track('browser_loaded', context);
    });
  }
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link className={clsx('button button--secondary button--lg', styles.linkButton)} to="commvault/commvault-public-cloud/Commvault_FAQ">Commvault</Link>
          <Link className={clsx('button button--secondary button--lg', styles.linkButton)} to="databunker/intro">Databunker</Link>
          <Link className={clsx('button button--secondary button--lg', styles.linkButton)} to="fire/fire-on-prem/intro">Fire</Link>
        </div>
      </div>
    </header>

  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
